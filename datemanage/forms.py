from django import forms
from .models import Employeetable, Attendancetable, Bonustable, Employeebonustable, Performanceevaluationtable, Performancetable, Workdaytable

class EmployeetableForm(forms.ModelForm):
    class Meta:
        model = Employeetable
        fields = ['name', 'gender', 'phonenumber']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phonenumber': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AttendancetableForm(forms.ModelForm):
    class Meta:
        model = Attendancetable
        fields = ['employeeid', 'date', 'clockintime', 'clockouttime']
        widgets = {
            'employeeid': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.Select(attrs={'class': 'form-control'}),
            'clockintime': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'clockouttime': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }







class PerformanceevaluationtableForm(forms.ModelForm):
    class Meta:
        model = Performanceevaluationtable
        fields = ['employeeid', 'indicatorname', 'score', 'evaluationdate']
        widgets = {
            'employeeid': forms.Select(attrs={'class': 'form-control'}),
            'indicatorname': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
            'evaluationdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class PerformancetableForm(forms.ModelForm):
    class Meta:
        model = Performancetable
        fields = ['indicatorname', 'weight']
        widgets = {
            'indicatorname': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class WorkdaytableForm(forms.ModelForm):
    class Meta:
        model = Workdaytable
        fields = ['date', 'isworkday']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'isworkday': forms.Select(choices=[(1, '是'), (0, '否')], attrs={'class': 'form-control'}),
        }


from django import forms
from .models import Bonustable

class BonustableForm(forms.ModelForm):
    class Meta:
        model = Bonustable
        fields = ['bonusid', 'amount', 'paymentdate', 'reason']
        widgets = {
            'bonusid': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'paymentdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class EmployeebonustableForm(forms.ModelForm):
    class Meta:
        model = Employeebonustable
        fields = ['employee', 'bonus', 'amount', 'paymentdate', 'reason']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'bonus': forms.HiddenInput(),  # 如果这个字段不应该显示给用户
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'paymentdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }