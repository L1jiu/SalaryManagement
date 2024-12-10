from django.urls import path
from . import views

app_name = 'datemanage'
urlpatterns = [
    path('datemanage/', views.datemanage, name='datemanage'),  # 员工信息管理

]