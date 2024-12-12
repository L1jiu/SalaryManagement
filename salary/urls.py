from django.urls import path
from . import views

app_name = 'salary'
urlpatterns = [
    path('salary/grosssalary', views.grosssalary, name='grosssalary'),

    path('salary/netsalary', views.netsalary, name='netsalary'),

    path('salary/export-to-excel', views.export_to_excel, name='export_to_excel'),

]