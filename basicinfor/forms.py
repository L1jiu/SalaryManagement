from django import forms
from .models import Employeetable
from .models import Positiontable

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employeetable
        fields = ['name', 'gender', 'phonenumber']

class PositionForm(forms.ModelForm):
    class Meta:
        model = Positiontable
        fields = ['positionname', 'basesalary']