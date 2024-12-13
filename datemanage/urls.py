from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import path

from datemanage.models import Employeebonustable
from . import views  # 导入视图模块

app_name = 'datemanage'  # 添加命名空间

def delete_employee_bonus(request, employee_id, bonus_id):
    if request.method == 'POST':
        try:
            eb = get_object_or_404(Employeebonustable, employee_id=employee_id, bonus_id=bonus_id)
            eb.delete()
            messages.success(request, '奖金信息已成功删除')
        except Exception as e:
            messages.error(request, f'删除失败: {e}')
        return redirect('datemanage:combined_bonuses')  # 假设这是你的URL名称

urlpatterns = [
    # 考勤管理路由
    path('attendance/', views.attendance_management, name='attendance_management'),

    # 绩效评估管理路由
    path('performance/', views.performance_evaluation_management, name='performance_evaluation_management'),

    # 员工奖金管理路由
    path('employee_bonus_management/', views.employee_bonus_management, name='employee_bonus_management'),
]