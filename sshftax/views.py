from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def sshftax(request):
    return HttpResponse("这是国家相关事务管理页面")