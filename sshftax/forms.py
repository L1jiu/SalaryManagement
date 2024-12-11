from django import forms
from .models import Employeetable, Employeetaxtable, Employeesocialsecurityandhousingfundtable

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employeetable
        fields = ['name', 'gender', 'phonenumber']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.TextInput(attrs={'class': 'form-control'}),
            'phonenumber': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EmployeeTaxForm(forms.ModelForm):
    class Meta:
        model = Employeetaxtable
        fields = ['employeeid', 'taxname', 'taxamount', 'paymentdate']
        labels = {
            'employeeid': '员工',
            'taxname': '税种名称',
            'taxamount': '税额',
            'paymentdate': '支付日期'
        }
        widgets = {
            'employeeid': forms.Select(attrs={'class': 'form-control'}),
            'taxname': forms.TextInput(attrs={'class': 'form-control'}),
            'taxamount': forms.NumberInput(attrs={'class': 'form-control'}),
            'paymentdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class EmployeeSocialSecurityAndHousingFundForm(forms.ModelForm):
    class Meta:
        model = Employeesocialsecurityandhousingfundtable
        fields = ['employeeid', 'projectname', 'amountdue', 'paymentdate', 'contributionrate']
        labels = {
            'employeeid': '员工',
            'projectname': '项目名称',
            'amountdue': '应缴金额',
            'paymentdate': '支付日期',
            'contributionrate': '缴费比例'
        }
        widgets = {
            'employeeid': forms.Select(attrs={'class': 'form-control'}),
            'projectname': forms.TextInput(attrs={'class': 'form-control'}),
            'amountdue': forms.NumberInput(attrs={'class': 'form-control'}),
            'paymentdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'contributionrate': forms.NumberInput(attrs={'class': 'form-control'}),
        }