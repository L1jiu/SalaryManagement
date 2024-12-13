from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from .forms import BonustableForm, EmployeebonustableForm, AddBonusAndAssignForm
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

from django.utils.dateformat import format  # 引入 Django 的日期格式化工具

# 初始化日志记录器
logger = logging.getLogger(__name__)
def attendance_management(request):
    if request.method == 'POST':
        try:
            # 获取请求的JSON数据
            data = json.loads(request.body.decode('utf-8'))
            action = data.get('action', '').strip().lower()  # 获取操作类型（添加、更新、删除）
            employee_id = data.get('employeeid')  # 员工ID
            date = data.get('date')  # 考勤日期
            clock_in_time = data.get('clockin_time')  # 上班时间
            clock_out_time = data.get('clockout_time')  # 下班时间

            logger.info(f"Received POST data: action={action}, employee_id={employee_id}, date={date}, "
                        f"clock_in_time={clock_in_time}, clock_out_time={clock_out_time}")

            # 检查必填字段是否完整
            if not all([employee_id, date, clock_in_time, clock_out_time]):
                error_message = "Employee ID, Date, Clock In Time, and Clock Out Time are required."
                logger.error(error_message)
                return JsonResponse({'status': 'error', 'errors': error_message}, status=400)

            # 添加操作
            if action == 'add':
                # 获取员工和日期对象
                employee = get_object_or_404(Employeetable, employeeid=employee_id)
                workday = get_object_or_404(Workdaytable, date=date)

                # 检查是否已经有考勤记录（防止违反唯一性约束）
                existing_attendance = Attendancetable.objects.filter(employeeid=employee, date=workday).first()
                if existing_attendance:
                    error_message = 'Attendance record already exists for this employee on the selected date.'
                    logger.error(error_message)
                    return JsonResponse({'status': 'error', 'errors': error_message}, status=400)

                # 创建新考勤记录
                new_attendance = Attendancetable.objects.create(
                    employeeid=employee,
                    date=workday,
                    clockintime=clock_in_time,
                    clockouttime=clock_out_time
                )
                logger.info(f"Added new attendance record: {new_attendance}")
                return JsonResponse({'status': 'success', 'message': 'Attendance record added successfully',
                                     'new_record_id': new_attendance.recordid})

            else:
                error_message = 'Invalid action specified.'
                logger.error(error_message)
                return JsonResponse({'status': 'error', 'errors': error_message}, status=400)

        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {e}")
            return JsonResponse({'status': 'error', 'errors': 'Invalid JSON format.'}, status=400)

        except Exception as e:
            logger.error(f"An error occurred during attendance management: {e}")
            return JsonResponse({'status': 'error', 'errors': str(e)}, status=500)

    else:
        # 如果是GET请求，返回所有考勤记录并渲染视图
        attendances = Attendancetable.objects.select_related('employeeid', 'date').all()  # 使用select_related优化查询

        # 格式化日期到 YYYY-MM-DD 格式
        formatted_attendances = []
        for attendance in attendances:
            formatted_attendances.append({
                'employeeid': attendance.employeeid,
                'employee_name': attendance.employeeid.name,
                'date': format(attendance.date.date, 'Y-m-d'),  # 确保输出的日期为字符串格式
                'clockintime': attendance.clockintime,
                'clockouttime': attendance.clockouttime,
                'id': attendance.recordid,
            })

        context = {
            'attendances': formatted_attendances,
            'view_type': 'attendances'
        }
        return render(request, 'attendance_management.html', context)


def performance_evaluation_management(request):
    try:
        # 获取所有绩效考核记录
        performance_records = Performanceevaluationtable.objects.all()

        # 查询每个绩效记录对应的员工姓名
        for record in performance_records:
            # 使用外键查询员工姓名
            employee = Employeetable.objects.get(employeeid=record.employeeid)
            # 将员工姓名添加到绩效记录中
            record.employee_name = employee.name

        # 添加日志输出检查数据是否正确
        logger.info(f"获取到的绩效考核记录: {performance_records}")

        # 渲染模板并传递数据
        context = {'performance_records': performance_records, 'view_type': 'performance'}
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
                return JsonResponse({'status': 'success'})
            except Exception as e:
                logger.error(f"Error deleting record: {e}")
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

        else:
            logger.warning("Received unknown POST operation.")
            return HttpResponseBadRequest("未知的操作")

    else:
        logger.warning("Received unsupported HTTP method.")
        return HttpResponseBadRequest("不支持的方法")