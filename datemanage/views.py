from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from .forms import BonustableForm, EmployeebonustableForm, AddBonusAndAssignForm, PerformanceevaluationtableForm, \
    AttendancetableForm
from .models import Employeebonustable, Bonustable, Employeetable


from .models import (
    Employeetable,
    Attendancetable,
    Workdaytable,
    Performanceevaluationtable,
    Employeebonustable,
    Bonustable
)


from django.utils.dateformat import format  # 引入 Django 的日期格式化工具

# 初始化日志记录器
logger = logging.getLogger(__name__)

def attendance_management(request):
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # 检查是否为AJAX请求
            if request.POST.get('action') == 'delete':
                record_id = request.POST.get('recordid')
                try:
                    record = Attendancetable.objects.get(pk=record_id)
                    record.delete()
                    return JsonResponse({'status': 'success'})
                except Attendancetable.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Record not found.'})
            elif request.POST.get('action') == 'add':
                form = AttendancetableForm(request.POST)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'status': 'success'})
                else:
                    errors = form.errors.as_json()
                    return JsonResponse({'status': 'error', 'message': errors}, status=400)
        else:
            form = AttendancetableForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('datemanage:attendance_management')

    form = AttendancetableForm()
    attendances = Attendancetable.objects.select_related('employeeid', 'date').all()

    context = {
        'form': form,
        'attendances': attendances,
    }
    return render(request, 'attendance_management.html', context)




def performance_evaluation_management(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = PerformanceevaluationtableForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # 保存新的绩效考核记录
                    new_record = form.save()

                    # 获取员工姓名并关联到新记录
                    employee = Employeetable.objects.get(employeeid=new_record.employeeid)
                    new_record.employee_name = employee.name

                    logger.info(f"成功添加了绩效考核记录: {new_record}")
                    return JsonResponse({'status': 'success', 'record': {
                        'employee_name': new_record.employee_name,
                        'employeeid': new_record.employeeid,
                        'indicatorname': new_record.indicatorname.indicatorname,
                        'score': str(new_record.score),
                        'evaluationdate': new_record.evaluationdate.strftime('%Y-%m-%d')
                    }})
            except Exception as e:
                logger.error(f"添加绩效考核记录时出错: {e}")
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        else:
            errors = form.errors.as_json()
            logger.error(f"表单验证失败: {errors}")
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

    try:
        # 获取所有绩效考核记录
        performance_records = Performanceevaluationtable.objects.all().select_related('indicatorname')

        # 查询每个绩效记录对应的员工姓名
        for record in performance_records:
            # 使用外键查询员工姓名
            employee = Employeetable.objects.get(employeeid=record.employeeid)
            # 将员工姓名添加到绩效记录中
            record.employee_name = employee.name

        # 添加日志输出检查数据是否正确
        logger.info(f"获取到的绩效考核记录: {performance_records}")

        # 渲染模板并传递数据
        context = {
            'performance_records': performance_records,
            'view_type': 'performance',
            'form': PerformanceevaluationtableForm()  # 为模态框提供表单
        }
        return render(request, 'performance_evaluation_management.html', context)

    except Exception as e:
        logger.error(f"绩效考核管理出现错误：{e}")
        return JsonResponse({'status': 'error', 'errors': str(e)}, status=500)


from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .models import Bonustable, Employeebonustable

import logging


def employee_bonus_management(request):
    if request.method == 'GET':
        # 获取所有员工奖金记录，并关联员工和奖金信息
        employee_bonuses = Employeebonustable.objects.select_related('employee', 'bonus').all()
        form = AddBonusAndAssignForm()
        return render(request, 'bonus.html', {
            'employee_bonuses': employee_bonuses,
            'form': form,
        })

    elif request.method == 'POST':
        if 'add_and_assign_bonus' in request.POST:
            form = AddBonusAndAssignForm(request.POST)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        # 创建 Bonustable 记录并保存
                        bonus = form.save()  # 这里直接保存 Bonus 对象

                        # 获取选定的员工对象
                        employee = form.cleaned_data['employee']

                        # 创建 Employeebonustable 记录
                        eb = Employeebonustable(
                            employee=employee,
                            bonus=bonus,
                            amount=bonus.amount,
                            paymentdate=bonus.paymentdate,
                            reason=bonus.reason
                        )
                        eb.save()

                        messages.success(request, "奖金已成功添加并分配给员工。")
                        return redirect('datemanage:employee_bonus_management')
                except Exception as e:
                    logger.error(f"Error adding and assigning bonus: {e}")
                    messages.error(request, "添加奖金时发生错误，请稍后再试。")

            else:
                # 表单验证失败，返回带有错误信息的页面
                employee_bonuses = Employeebonustable.objects.select_related('employee', 'bonus').all()
                return render(request, 'bonus.html', {
                    'employee_bonuses': employee_bonuses,
                    'form': form,
                }, status=400)

        elif 'delete_bonus' in request.POST:
            employee_id = request.POST.get('employee_id')
            bonus_id = request.POST.get('bonus_id')

            logger.debug(f"Received delete request with employee_id: {employee_id}, bonus_id: {bonus_id}")

            if not (employee_id and bonus_id):
                return JsonResponse({'status': 'error', 'message': '缺少必要的参数'}, status=400)

            try:
                eb = get_object_or_404(Employeebonustable, employee_id=employee_id, bonus__BonusID=bonus_id)
                eb.delete()
                logger.info(f"Successfully deleted record for employee_id: {employee_id}, bonus_id: {bonus_id}")
                return redirect('datemanage:employee_bonus_management')
            except Exception as e:
                logger.error(f"Error deleting record: {e}")
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

        else:
            logger.warning("Received unknown POST operation.")
            return HttpResponseBadRequest("未知的操作")

    else:
        logger.warning("Received unsupported HTTP method.")
        return HttpResponseBadRequest("不支持的方法")