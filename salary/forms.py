from django import forms
from .models import Attendancetable, Bonustable, Employeebonustable, Employeepositiontable, Employeesocialsecurityandhousingfundtable, Employeetable, Employeetaxtable, Grosssalary, Performanceevaluationtable, Performancetable, Positiontable, Socialsecurityandhousingfundtable, Taxtable, Workdaytable

# 出勤表单
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendancetable
        fields = ['employeeid', 'date', 'clockintime', 'clockouttime']

# 奖金表单
class BonusForm(forms.ModelForm):
    class Meta:
        model = Bonustable
        fields = ['amount', 'paymentdate', 'reason']

# 员工奖金表单
class EmployeeBonusForm(forms.ModelForm):
    class Meta:
        model = Employeebonustable
        fields = ['bonusid', 'amount', 'paymentdate', 'reason']

# 员工职位表单
class EmployeePositionForm(forms.ModelForm):
    class Meta:
        model = Employeepositiontable
        fields = ['positionname']

# 员工社保及住房基金表单
class EmployeeSocialSecurityAndHousingFundForm(forms.ModelForm):
    class Meta:
        model = Employeesocialsecurityandhousingfundtable
        fields = ['projectname', 'amountdue', 'paymentdate', 'contributionrate']

# 员工基本信息表单
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employeetable
        fields = ['name', 'gender', 'phonenumber']

# 员工税务表单
class EmployeeTaxForm(forms.ModelForm):
    class Meta:
        model = Employeetaxtable
        fields = ['taxname', 'taxamount', 'paymentdate']

# 毛工资表单
class GrossSalaryForm(forms.ModelForm):
    class Meta:
        model = Grosssalary
        fields = ['year', 'month', 'basesalary', 'absentdeduction', 'overtimepay', 'performancebonus', 'yearendbonus']

# 绩效评估表单
class PerformanceEvaluationForm(forms.ModelForm):
    class Meta:
        model = Performanceevaluationtable
        fields = ['indicatorname', 'score', 'evaluationdate']

# 绩效指标表单
class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performancetable
        fields = ['weight']

# 职位表单
class PositionForm(forms.ModelForm):
    class Meta:
        model = Positiontable
        fields = ['basesalary']

# 社保及住房基金项目表单
class SocialSecurityAndHousingFundForm(forms.ModelForm):
    class Meta:
        model = Socialsecurityandhousingfundtable
        fields = ['contributionrate']

# 税种表单
class TaxForm(forms.ModelForm):
    class Meta:
        model = Taxtable
        fields = ['lowerlimit', 'upperlimit', 'taxrate', 'quickdeduction']

# 工作日表单
class WorkdayForm(forms.ModelForm):
    class Meta:
        model = Workdaytable
        fields = ['isworkday']