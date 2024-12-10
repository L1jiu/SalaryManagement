from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def salary(request):
    return HttpResponse("这是工资统计分析页面")