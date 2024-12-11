from django.views.decorators.csrf import csrf_protect
import logging
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.csrf import csrf_protect

from .models import Employeetable, Attendancetable, Workdaytable, Performanceevaluationtable
from .models import Employeebonustable
# 设置日志记录
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



from django.shortcuts import render
from django.http import JsonResponse
from .models import Performanceevaluationtable, Employeetable
import logging

# 初始化日志
logger = logging.getLogger(__name__)

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


from django.shortcuts import get_object_or_404



from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Employeetable, Bonustable, Employeebonustable
import logging

logger = logging.getLogger(__name__)

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Employeetable, Employeebonustable
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def employee_bonus_management(request):
    # 查询所有员工信息（包括员工姓名等）
    employees = Employeetable.objects.all()

    # 处理POST请求（发放奖金）
    if request.method == "POST":
        try:
            # 获取请求体并打印调试信息
            raw_data = request.body.decode('utf-8')
            logger.info(f"Received POST data: {raw_data}")  # 打印接收到的原始数据

            # 尝试解析JSON数据
            data = json.loads(raw_data)
            employee_id = data.get('employeeid')
            bonus_id = data.get('bonusid')
            amount = data.get('amount')
            payment_date = data.get('paymentdate')
            reason = data.get('reason')

            # 数据验证
            if not all([employee_id, bonus_id, amount, payment_date, reason]):
                return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)

            # 验证金额格式是否有效
            try:
                amount = float(amount)  # 确保amount是浮动型数字
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'Invalid amount format.'}, status=400)

            # 获取员工记录
            employee = Employeetable.objects.get(employeeid=employee_id)

            # 创建奖金记录到 Employeebonustable 中
            Employeebonustable.objects.create(
                employee=employee,
                bonusid=bonus_id,
                amount=amount,
                paymentdate=payment_date,
                reason=reason
            )

            return JsonResponse({'status': 'success', 'message': 'Bonus record added successfully.'})

        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {e}")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    # GET请求（渲染奖金管理页面）
    return render(request, 'employee_bonus_management.html', {'employees': employees})
