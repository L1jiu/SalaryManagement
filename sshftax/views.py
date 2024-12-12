from django.shortcuts import render, get_object_or_404
from .models import Employeetable, Employeetaxtable, Employeesocialsecurityandhousingfundtable

def employee_list(request):
    employees = Employeetable.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

def employee_details(request, employee_id):
    employee = get_object_or_404(Employeetable, employeeid=employee_id)
    tax_records = Employeetaxtable.objects.filter(employeeid=employee_id)
    social_security_records = Employeesocialsecurityandhousingfundtable.objects.filter(employeeid=employee_id)
    return render(request, 'employee_details.html', {
        'employee': employee,
        'tax_records': tax_records,
        'social_security_records': social_security_records,
    })
