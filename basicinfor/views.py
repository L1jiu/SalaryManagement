from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Employeetable
from .models import Positiontable
from .forms import PositionForm  # 确保已定义PositionForm
import logging


logger = logging.getLogger(__name__)
@csrf_exempt  # 注意：仅用于测试，请确保生产环境中正确配置CSRF保护
def employee_management(request):
    if request.method == 'POST':
        try:
            action = request.POST.get('action')
            employee_id = request.POST.get('employeeid')
            name = request.POST.get('name')
            gender = request.POST.get('gender')
            phonenumber = request.POST.get('phonenumber')

            if not all([name, gender, phonenumber]) and action != 'delete':
                raise ValueError("All fields are required.")

            if action == 'delete':  # 删除操作
                if not employee_id:
                    return JsonResponse({'status': 'error', 'errors': 'Employee ID is required for deletion.'},
                                        status=400)

                employee_id = int(employee_id)
                employee = get_object_or_404(Employeetable, employeeid=employee_id)
                employee.delete()
                return JsonResponse({'status': 'success'})

            elif employee_id:  # 更新操作
                employee_id = int(employee_id)
                employee = get_object_or_404(Employeetable, employeeid=employee_id)
                employee.name = name
                employee.gender = gender
                employee.phonenumber = phonenumber
                employee.save()
                return JsonResponse({'status': 'success'})
            else:  # 添加操作
                new_employee = Employeetable.objects.create(
                    name=name,
                    gender=gender,
                    phonenumber=phonenumber
                )
                return JsonResponse({'status': 'success', 'new_employee_id': new_employee.employeeid})
        except ValueError as ve:
            return JsonResponse({'status': 'error', 'errors': str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'errors': str(e)}, status=500)

    else:
        employees = Employeetable.objects.all()
        context = {'employees': employees, 'view_type': 'employees'}
        return render(request, 'employee_management.html', context)


@csrf_exempt  # 注意：仅用于测试，请确保生产环境中正确配置CSRF保护
def position_management(request):
    if request.method == 'POST':
        action = request.POST.get('action', '').strip().lower()

        if action == 'delete':  # 删除操作
            positionname = request.POST.get('positionname')
            if not positionname:
                return JsonResponse({'status': 'error', 'errors': 'Position name is required for deletion.'},
                                    status=400)

            try:
                position = get_object_or_404(Positiontable, positionname=positionname)
                position.delete()
                return JsonResponse({'status': 'success'})
            except Exception as e:
                logger.error(f"An error occurred during position deletion: {e}")
                return JsonResponse({'status': 'error', 'errors': str(e)}, status=500)

        else:  # 添加或更新操作
            form = PositionForm(request.POST)

            if not form.is_valid():
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

            try:
                if action == 'update':  # 更新操作
                    positionname = form.cleaned_data.get('positionname')
                    basesalary = form.cleaned_data.get('basesalary')

                    if not all([positionname, basesalary]):
                        raise ValueError("All fields are required.")

                    position = get_object_or_404(Positiontable, positionname=positionname)
                    position.basesalary = basesalary
                    position.save()
                    return JsonResponse({'status': 'success'})

                else:  # 添加操作
                    new_position = form.save()  # 使用form保存新的职位信息
                    return JsonResponse({'status': 'success', 'new_position_name': new_position.positionname})

            except Exception as e:
                logger.error(f"An error occurred during position management: {e}")
                return JsonResponse({'status': 'error', 'errors': str(e)}, status=500)

    else:
        positions = Positiontable.objects.all()
        context = {'positions': positions, 'view_type': 'positions'}
        return render(request, 'position_management.html', context)