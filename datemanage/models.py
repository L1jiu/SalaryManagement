from django.db import models
from django.db.models import Q
class Employeetable(models.Model):
    employeeid = models.AutoField(db_column='EmployeeID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100)
    gender = models.CharField(db_column='Gender', max_length=6)
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'employeetable'

class Attendancetable(models.Model):
    recordid = models.AutoField(db_column='RecordID', primary_key=True)
    employeeid = models.ForeignKey('Employeetable', on_delete=models.CASCADE, db_column='EmployeeID')  # 修改为 CASCADE 或其他适合的删除行为
    date = models.ForeignKey('Workdaytable', on_delete=models.CASCADE, db_column='Date')  # 修改为 CASCADE 或其他适合的删除行为
    clockintime = models.TimeField(db_column='ClockInTime', blank=True, null=True)
    clockouttime = models.TimeField(db_column='ClockOutTime', blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'attendancetable'
        unique_together = (('employeeid', 'date'),)


class Bonustable(models.Model):
    BonusID = models.AutoField(primary_key=True, db_column='BonusID')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paymentdate = models.DateField()
    reason = models.TextField()

    class Meta:
        db_table = 'bonustable'






class Performanceevaluationtable(models.Model):
    employeeid = models.IntegerField(db_column='EmployeeID', primary_key=True)  # Field name made lowercase.
    indicatorname = models.ForeignKey('Performancetable', on_delete=models.DO_NOTHING, db_column='IndicatorName')
    score = models.DecimalField(db_column='Score', max_digits=5, decimal_places=2)
    evaluationdate = models.DateField(db_column='EvaluationDate')

    def get_employee_name(self):
        try:
            return Employeetable.objects.get(employeeid=self.employeeid).name
        except Employeetable.DoesNotExist:
            return "未知员工"

    class Meta:
        managed = False
        db_table = 'performanceevaluationtable'
        unique_together = (('employeeid', 'indicatorname', 'evaluationdate'),)


class Performancetable(models.Model):
    indicatorname = models.CharField(db_column='IndicatorName', primary_key=True, max_length=100)
    weight = models.DecimalField(db_column='Weight', max_digits=5, decimal_places=2)

    def __str__(self):
        return self.indicatorname

    class Meta:
        managed = False
        db_table = 'performancetable'


class Employeebonustable(models.Model):
    id = models.AutoField(primary_key=True)  # 显式声明主键字段
    employee = models.ForeignKey(Employeetable, on_delete=models.CASCADE, db_column='EmployeeID')
    bonus = models.ForeignKey(Bonustable, on_delete=models.CASCADE, db_column='BonusID')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paymentdate = models.DateField()
    reason = models.TextField()

    class Meta:
        db_table = 'employeebonustable'


class Workdaytable(models.Model):
    date = models.DateField(db_column='Date', primary_key=True)
    isworkday = models.IntegerField(db_column='IsWorkday')

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')

    class Meta:
        managed = False
        db_table = 'workdaytable'

