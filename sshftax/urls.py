from django.urls import path
from . import views

app_name = 'sshftax'
urlpatterns = [
    path('sshftax/', views.sshftax, name='sshftax'),

]