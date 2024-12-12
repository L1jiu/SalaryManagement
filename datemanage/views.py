from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import json
import logging


# 初始化日志记录器
logger = logging.getLogger(__name__)

from .models import (
    Employeetable,
    Attendancetable,
    Workdaytable,
    Performanceevaluationtable,
    Employeebonustable,
    Bonustable
)

@csrf_exempt
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
                return JsonResponse({'status': 'success', 'message': 'Attendance record added successfully', 'new_record_id': new_attendance.recordid})

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
        context = {
            'attendances': attendances,
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


def employee_bonus_management(request):
    if request.method == "GET":
        # 查询所有员工信息（包括员工姓名等）
        employees = Employeetable.objects.all()

        # 构建一个包含员工及其奖金记录的列表
        employee_data = []
        for employee in employees:
            employee_bonuses = Employeebonustable.objects.filter(employee=employee)
            employee_data.append({
                'employee': employee,
                'bonuses': employee_bonuses
            })

        return render(request, 'employee_bonus_management.html', {
            'employee_data': employee_data  # 包含员工及对应奖金记录的数据
        })

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            action = data.get('action', '').lower()

            if action == 'delete':
                bonus_id = data.get('bonusid')
                if not bonus_id:
                    return JsonResponse({'status': 'error', 'message': 'Bonus ID is required for deletion.'},
                                        status=400)

                deleted_count, _ = Employeebonustable.objects.filter(bonusid=bonus_id).delete()
                if deleted_count > 0:
                    return JsonResponse({'status': 'success', 'message': 'Bonus record deleted successfully.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Bonus record not found.'}, status=404)

            else:  # 假设其他动作是添加新的奖金记录
                employee_id = data.get('employeeid')
                bonus_id = data.get('bonusid')
                amount = data.get('amount')
                payment_date = data.get('paymentdate')
                reason = data.get('reason')

                if not all([employee_id, bonus_id, amount, payment_date, reason]):
                    return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)

                try:
                    amount = float(amount)  # 确保金额是浮点数
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': 'Invalid amount format.'}, status=400)

                try:
                    employee = Employeetable.objects.get(employeeid=employee_id)
                except Employeetable.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Employee does not exist.'}, status=400)

                Employeebonustable.objects.create(
                    employee=employee,
                    bonusid=bonus_id,
                    amount=amount,
                    paymentdate=payment_date,
                    reason=reason
                )

                return JsonResponse({'status': 'success', 'message': 'Bonus record added successfully.'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Bonustable
from .forms import BonustableForm  # 使用新定义的表单类

def combined_bonuses(request):
    bonuses = Bonustable.objects.all().order_by('-paymentdate')

    if request.method == 'POST':
        if 'add_bonus' in request.POST:
            form = BonustableForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Bonus added successfully.')
                return redirect('datemanage:combined_bonuses')  # 使用命名空间和连字符
            else:
                messages.error(request, 'Please correct the errors below.')
        elif 'delete_bonus' in request.POST:
            bonus_id = request.POST.get('bonus_id')
            if bonus_id:
                try:
                    bonus = Bonustable.objects.get(pk=bonus_id)
                    bonus.delete()
                    messages.success(request, 'Bonus deleted successfully.')
                except Bonustable.DoesNotExist:
                    messages.error(request, 'The specified bonus does not exist.')
            else:
                messages.error(request, 'No bonus ID provided.')
            return redirect('datemanage:combined_bonuses')  # 使用命名空间和连字符
    else:
        form = BonustableForm()

    context = {
        'bonuses': bonuses,
        'form': form,
    }

    return render(request, 'combined_bonus.html', context)