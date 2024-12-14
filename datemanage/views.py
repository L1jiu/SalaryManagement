import json

from django.contrib import messages
from django.db import transaction, IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
import logging

from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from .forms import BonustableForm, EmployeebonustableForm, AddBonusAndAssignForm, PerformanceevaluationtableForm, \
    AttendancetableForm

from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EmployeeSerializer, PerformanceSerializer


from .models import (
    Employeetable,
    Attendancetable,
    Workdaytable,
    Performanceevaluationtable,
    Employeebonustable,
    Bonustable,
    Performancetable
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
    if request.method == 'POST':
        try:
            # 从请求体中解析JSON数据
            body = json.loads(request.body)
            employeeid = body.get('employeeid')
            indicatorname = body.get('indicatorname')
            score = body.get('score')
            evaluationdate = body.get('evaluationdate')

            if not all([employeeid, indicatorname, score, evaluationdate]):
                return JsonResponse({'status': 'error', 'message': '缺少必要的参数'}, status=400)

            Performanceevaluationtable.objects.create(
                employeeid=employeeid,
                indicatorname=indicatorname,
                score=score,
                evaluationdate=evaluationdate
            )
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的JSON格式'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    if request.method == 'DELETE':

        try:

            # 从请求体中解析JSON数据

            body = json.loads(request.body)

            employee_name = body.get('employeeName')

            indicator_name = body.get('indicatorName')

            evaluation_date = body.get('evaluationDate')

            # 验证所有必要参数是否都存在

            if not all([employee_name, indicator_name, evaluation_date]):
                return JsonResponse({'status': 'error', 'message': '缺少必要的参数'}, status=400)

            # 根据员工名字查询employeeid

            try:

                employee = Employeetable.objects.get(Name=employee_name)

            except Employeetable.DoesNotExist:

                return JsonResponse({'status': 'error', 'message': '找不到对应的员工'}, status=404)

            # 查询Performancetable以获取IndicatorName的实例

            try:

                indicator = Performancetable.objects.get(IndicatorName=indicator_name)

            except Performancetable.DoesNotExist:

                return JsonResponse({'status': 'error', 'message': '找不到对应的绩效指标'}, status=404)

            # 尝试直接使用传入的日期字符串（假设它已经是正确格式）

            try:

                evaluation_date = timezone.datetime.strptime(evaluation_date, '%Y-%m-%d').date()

            except ValueError:

                return JsonResponse({'status': 'error', 'message': '日期格式错误'}, status=400)

            # 直接查询Performanceevaluationtable并删除记录

            deleted_count, _ = Performanceevaluationtable.objects.filter(

                EmployeeID=employee.employeeid,

                IndicatorName=indicator,  # 使用indicator对象而不是字符串

                EvaluationDate=evaluation_date

            ).delete()

            if deleted_count == 0:

                return JsonResponse({'status': 'error', 'message': '没有找到可删除的记录'}, status=404)

            else:

                return JsonResponse({'status': 'success', 'message': f'成功删除了 {deleted_count} 条记录'})


        except json.JSONDecodeError:

            return JsonResponse({'status': 'error', 'message': 'DELETE:无效的JSON格式'}, status=400)

        except Exception as e:

            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    else:  # GET请求
        # 获取所有绩效记录并传递给模板
        performance_records = Performanceevaluationtable.objects.select_related('indicatorname').all()
        context = {
            'performance_records': performance_records,
            'employees': Employeetable.objects.all(),
            'indicators': Performancetable.objects.all(),
        }
        return render(request, 'performance_evaluation_management.html', context)


@api_view(['GET'])
def employee_list_api(request):
    employees = Employeetable.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def performance_list_api(request):
    performances = Performancetable.objects.all()
    serializer = PerformanceSerializer(performances, many=True)
    return Response(serializer.data)






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