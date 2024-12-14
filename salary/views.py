from io import BytesIO
from urllib.parse import quote

import pandas as pd
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.db.models import Sum, F, DecimalField, Value, Avg
from django.db.models.functions import Coalesce
from django.db.models.expressions import ExpressionWrapper
from django.views.decorators.csrf import csrf_exempt

from .models import Grosssalary, Employeetable, Positiontable
import json
from django.db import connection, connections, DatabaseError
from .models import get_salary_view_model
from django.utils import timezone
from django.db.models import Avg, Max, Min, Sum, Count
import logging

# 配置日志
logger = logging.getLogger(__name__)


def grosssalary(request):
    # 获取所有不同的年份
    years = Grosssalary.objects.values_list('year', flat=True).distinct().order_by('-year')

    # 构造数字月份列表，而非中文月份
    months = [str(i).zfill(2) for i in range(1, 13)]  # ['01', '02', ..., '12']

    selected_year = request.GET.get('year')
    selected_month_str = request.GET.get('month')

    filter_query = {}
    if selected_year:
        filter_query['year'] = int(selected_year)

    if selected_month_str and selected_month_str.isdigit():
        selected_month = int(selected_month_str)
        if 1 <= selected_month <= 12:
            filter_query['month'] = selected_month

    salaries = (Grosssalary.objects.filter(**filter_query)
                .annotate(
        total_gross_salary=ExpressionWrapper(
            Coalesce(F('basesalary__basesalary'), Value(0, output_field=DecimalField())) -
            Coalesce(F('absentdeduction'), Value(0, output_field=DecimalField())) +
            Coalesce(F('overtimepay'), Value(0, output_field=DecimalField())) +
            Coalesce(F('performancebonus'), Value(0, output_field=DecimalField())) +
            Coalesce(F('yearendbonus'), Value(0, output_field=DecimalField())),
            output_field=DecimalField()
        )
    )
                .select_related('employeeid', 'basesalary')  # 确保也选择了 basesalary 关联的数据
                .order_by('employeeid__employeeid', 'month'))

    # 准备用于图表的数据
    chart_data = {}

    if not selected_month_str:  # 只有在不是单个月份查询时才生成折线图数据
        for salary in salaries:
            employee_id = salary.employeeid.employeeid
            if employee_id not in chart_data:
                chart_data[employee_id] = {
                    'label': salary.employeeid.name,
                    'data': [0] * 12  # 初始化每个月的数据为0
                }
            month_index = salary.month - 1
            chart_data[employee_id]['data'][month_index] = float(salary.total_gross_salary or 0)
    else:
        for salary in salaries:
            employee_id = salary.employeeid.employeeid
            if employee_id not in chart_data:
                chart_data[employee_id] = {
                    'label': salary.employeeid.name,
                    'data': [float(salary.total_gross_salary or 0)]  # 单个月份的数据
                }

    chart_json = json.dumps(list(chart_data.values()), cls=DjangoJSONEncoder)

    context = {
        'years': years,
        'months': months,
        'salaries': salaries,
        'selected_year': selected_year,
        'selected_month': selected_month_str,
        'chart_data': chart_json
    }
    return render(request, 'grosssalary.html', context)


def get_chart_data(salaries):
    labels = []  # 图表X轴标签，这里使用员工姓名
    data = []  # 图表Y轴数据，这里使用净工资数值

    for salary in salaries:
        labels.append(salary.employeeid.name)
        data.append(float(salary.netsalary))  # 确保转换为float类型以避免JSON序列化问题

    chart_data = {
        'labels': labels,
        'datasets': [{
            'label': '净工资',
            'data': data,
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1
        }]
    }

    return chart_data


def netsalary(request):
    selected_year_month = request.GET.get('year_month') or request.POST.get('year_month') or timezone.now().strftime('%Y_%m')
    selected_year_month_display = selected_year_month.replace('_', '-')  # 用于显示

    SalaryView = get_salary_view_model(selected_year_month)

    salaries = None
    avg_netsalary = max_netsalary = min_netsalary = total_netsalary = employee_count = avg_basesalary = None
    chart_data = {}

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        with connection.cursor() as cursor:
            cursor.callproc('CalculateNetSalary', [selected_year_month_display])
        messages.success(request, f'已成功重新计算 {selected_year_month_display} 的工资。')

        try:
            salaries = SalaryView.objects.all()
            stats = salaries.aggregate(
                avg_netsalary=Avg('netsalary'),
                max_netsalary=Max('netsalary'),
                min_netsalary=Min('netsalary'),
                total_netsalary=Sum('netsalary'),
                employee_count=Count('employeeid'),
                avg_basesalary=Avg('basesalary')
            )
            avg_netsalary = stats['avg_netsalary']
            max_netsalary = stats['max_netsalary']
            min_netsalary = stats['min_netsalary']
            total_netsalary = stats['total_netsalary']
            employee_count = stats['employee_count']
            avg_basesalary = stats['avg_basesalary']

            chart_data = get_chart_data(salaries)
        except Exception as e:
            messages.error(request, f'查询工资数据时出错: {e}')

        context = {
            'salaries': list(salaries.values()),  # 将QuerySet转换为列表
            'selected_year_month': selected_year_month_display,
            'avg_netsalary': round(avg_netsalary, 2) if avg_netsalary else None,
            'max_netsalary': max_netsalary,
            'min_netsalary': min_netsalary,
            'total_netsalary': total_netsalary,
            'employee_count': employee_count,
            'avg_basesalary': round(avg_basesalary, 2) if avg_basesalary else None,
            'chart_data': chart_data,
        }
        return JsonResponse(context, encoder=DjangoJSONEncoder)

    elif request.method == 'POST':
        return redirect('salary:netsalary')

    try:
        if request.GET.get('action') == 'calculate':
            pass  # 这里可以添加额外逻辑

        salaries = SalaryView.objects.all()

        stats = salaries.aggregate(
            avg_netsalary=Avg('netsalary'),
            max_netsalary=Max('netsalary'),
            min_netsalary=Min('netsalary'),
            total_netsalary=Sum('netsalary'),
            employee_count=Count('employeeid'),
            avg_basesalary=Avg('basesalary')
        )
        avg_netsalary = stats['avg_netsalary']
        max_netsalary = stats['max_netsalary']
        min_netsalary = stats['min_netsalary']
        total_netsalary = stats['total_netsalary']
        employee_count = stats['employee_count']
        avg_basesalary = stats['avg_basesalary']

        chart_data = get_chart_data(salaries)
    except Exception as e:
        messages.error(request, f'查询工资数据时出错: {e}')

    context = {
        'salaries': salaries,
        'selected_year_month': selected_year_month_display,
        'avg_netsalary': round(avg_netsalary, 2) if avg_netsalary else None,
        'max_netsalary': max_netsalary,
        'min_netsalary': min_netsalary,
        'total_netsalary': total_netsalary,
        'employee_count': employee_count,
        'avg_basesalary': round(avg_basesalary, 2) if avg_basesalary else None,
        'chart_data': json.dumps(chart_data),  # 将图表数据转换为JSON字符串
    }

    return render(request, 'netsalary.html', context)

FIELD_NAME_MAP = {
    'id': 'ID',
    'employeeid': '员工编号',
    'basesalary': '基本工资',
    'netsalary': '净工资',
    'year_month': '年月',
    'name':'姓名',
    'absentdeduction':'缺勤扣款',
    'overtimepay':'加班工资',
    'performancebonus':'绩效奖金',
    'yearendbonus':'年终奖',
    'socialsecurityandhousingfund':'五险一金扣除',
    'incometax':'个税扣除'
}


@csrf_exempt
def export_to_excel(request):
    selected_year_month = request.GET.get('year_month') or timezone.now().strftime('%Y_%m')
    selected_year_month_display = selected_year_month.replace('_', '-')  # 用于显示
    logger.info(f"Selected year-month for export: {selected_year_month}")

    try:
        SalaryView = get_salary_view_model(selected_year_month)
        salaries = SalaryView.objects.all()

        if not salaries.exists():
            logger.warning(f'No salary data found for export in {selected_year_month}. Returning 404.')
            raise Http404("没有找到工资数据进行导出。")

        # 获取原始数据并重命名列
        df = pd.DataFrame(list(salaries.values()))
        df.rename(columns=FIELD_NAME_MAP, inplace=True)

        output = BytesIO()
        sheet_name = f'净工资-{selected_year_month}'
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
            writer.close()  # 确保所有数据都被写入到output中

        # 动态生成文件名，并使用quote进行URL编码
        file_name = f'净工资-{selected_year_month_display}.xlsx'
        encoded_filename = quote(file_name)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # 设置Content-Disposition头部，确保兼容性
        response[
            'Content-Disposition'] = f'attachment; filename="{encoded_filename}"; filename*=UTF-8\'\'{encoded_filename}'

        response.write(output.getvalue())
        return response

    except Http404:
        raise  # 让Django处理404异常
    except Exception as e:
        logger.error(f'Error exporting salary data: {e}', exc_info=True)
        messages.error(request, f'导出工资数据时出错: {e}')
        return redirect('salary:netsalary')