from django.urls import path
from . import views  # 导入视图模块

app_name = 'attendance'  # 添加命名空间

urlpatterns = [
    # 考勤管理路由
    path('attendance/', views.attendance_management, name='attendance_management'),

    # 绩效评估管理路由
    path('performance/', views.performance_evaluation_management, name='performance_evaluation_management'),

    # 员工奖金管理路由
    path('employee_bonus_management/', views.employee_bonus_management, name='employee_bonus_management'),
]
