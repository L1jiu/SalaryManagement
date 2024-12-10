from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def datemanage(request):
    return HttpResponse("这是日常事务管理页面")