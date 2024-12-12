from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Sum, F, DecimalField, Value, Avg
from django.db.models.functions import Coalesce
from django.db.models.expressions import ExpressionWrapper
from .models import Grosssalary, Employeetable, Positiontable
import json
from django.db import connection
from .models import get_salary_view_model
from django.utils import timezone
from django.db.models import Avg, Max, Min, Sum, Count


def grosssalary(request):
    # 获取所有不同的年份和月份，基于 year 和 month 字段
    years = Grosssalary.objects.values_list('year', flat=True).distinct().order_by('-year')
    months = [f'{i}月' for i in range(1, 13)]  # 构造中文月份列表

    selected_year = request.GET.get('year')
    selected_month_str = request.GET.get('month')

    filter_query = {}
    if selected_year:
        filter_query['year'] = int(selected_year)

    selected_month = None
    if selected_month_str:
        try:
            selected_month = int(selected_month_str.split('月')[0])  # 将月份转换为整数
            filter_query['month'] = selected_month
        except (ValueError, AttributeError):
            pass  # 如果转换失败，忽略错误并继续

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

    if not selected_month:  # 只有在不是单个月份查询时才生成折线图数据
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

    chart_json = json.dumps(list(chart_data.values()))

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
        labels.append(salary.name)
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