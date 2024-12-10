from django.urls import path
from . import views

app_name = 'salary'
urlpatterns = [
    path('salary/', views.salary, name='salary'),

]