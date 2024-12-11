from django.urls import path
from . import views

app_name = 'sshftax'  # Namespace for app URLs
urlpatterns = [
    path('sshftax/', views.employee_list, name='sshftax'),  # Updated to use the employee_list view
    path('sshftax/<int:employee_id>/', views.employee_details, name='employee_details'),  # Updated path
]
