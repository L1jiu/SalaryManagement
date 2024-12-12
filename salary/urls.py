from django.urls import path
from . import views

app_name = 'salary'
urlpatterns = [
    path('salary/grosssalary', views.grosssalary, name='grosssalary'),

    path('salary/netsalary', views.netsalary, name='netsalary'),

]