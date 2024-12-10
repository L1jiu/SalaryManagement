from django import forms
from .models import Employeetable
from .models import Positiontable
from .models import Employeepositiontable

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employeetable
        fields = ['name', 'gender', 'phonenumber']

class PositionForm(forms.ModelForm):
    class Meta:
        model = Positiontable
        fields = ['positionname', 'basesalary']

class EmployeePositionForm(forms.ModelForm):
    class Meta:
        model = Employeepositiontable
        fields = ['employeeid', 'positionname']
        labels = {
            'employeeid': '员工',
            'positionname': '职位',
        }
        widgets = {
            'employeeid': forms.Select(attrs={'class': 'form-control'}),
            'positionname': forms.Select(attrs={'class': 'form-control'}),
        }