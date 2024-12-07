from django.urls import path
from . import views

app_name = 'basicinfor'
urlpatterns = [
    path('basicinfor/employee', views.employee_management, name='employee_management'),  # 员工信息管理
     path('basicinfor/position', views.position_management, name='position_management'),  # 职位信息管理
]