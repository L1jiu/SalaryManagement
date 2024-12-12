from django.shortcuts import render
from django.db.models import Sum, F, DecimalField, Value
from django.db.models.functions import Coalesce
from django.db.models.expressions import ExpressionWrapper
from .models import Grosssalary, Employeetable, Positiontable
import json

def grosssalary(request):
    # 获取所有不同的年份，基于 year 字段
    years = Grosssalary.objects.values_list('year', flat=True).distinct().order_by('-year')

    selected_year = request.GET.get('year')
    if selected_year:
        selected_year = int(selected_year)
        salaries = (Grosssalary.objects.filter(year=selected_year)
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
    else:
        salaries = []

    # 准备用于图表的数据
    chart_data = {}
    for salary in salaries:
        employee_id = salary.employeeid.employeeid
        if employee_id not in chart_data:
            chart_data[employee_id] = {
                'name': salary.employeeid.name,
                'data': [0] * 12  # 初始化每个月的数据为0
            }
        month_index = salary.month - 1
        chart_data[employee_id]['data'][month_index] = float(salary.total_gross_salary or 0)

    chart_json = json.dumps([{'label': data['name'], 'data': data['data']} for data in chart_data.values()])

    context = {
        'years': years,
        'salaries': salaries,
        'selected_year': selected_year,
        'chart_data': chart_json
    }
    return render(request, 'grosssalary.html', context)