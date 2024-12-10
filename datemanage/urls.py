from django.urls import path
from . import views

app_name = 'datemanage'
#123
urlpatterns = [
    path('datemanage/', views.datemanage, name='datemanage'),  # 员工信息管理

]