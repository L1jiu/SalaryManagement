from django.db import models

class Employeetable(models.Model):
    employeeid = models.AutoField(db_column='EmployeeID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=6)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=20, blank=True, null=True)  # Field name made lowercase.

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
        unique_together = (('recordid', 'employeeid', 'date'),)


class Bonustable(models.Model):
    bonusid = models.AutoField(db_column='BonusID', primary_key=True)
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2)
    paymentdate = models.DateField(db_column='PaymentDate')
    reason = models.TextField(db_column='Reason', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bonustable'






class Performanceevaluationtable(models.Model):
    employeeid = models.IntegerField(db_column='EmployeeID', primary_key=True)  # Field name made lowercase.
    indicatorname = models.ForeignKey('Performancetable', on_delete=models.DO_NOTHING, db_column='IndicatorName')
    score = models.DecimalField(db_column='Score', max_digits=5, decimal_places=2)
    evaluationdate = models.DateField(db_column='EvaluationDate')

    class Meta:
        managed = False
        db_table = 'performanceevaluationtable'
        unique_together = (('employeeid', 'indicatorname', 'evaluationdate'),)


class Performancetable(models.Model):
    indicatorname = models.CharField(db_column='IndicatorName', primary_key=True, max_length=100)
    weight = models.DecimalField(db_column='Weight', max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'performancetable'

class Employeebonustable(models.Model):
    employee = models.ForeignKey('Employeetable', on_delete=models.CASCADE, db_column='EmployeeID')
    bonus = models.ForeignKey(Bonustable, on_delete=models.DO_NOTHING, db_column='BonusID')
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2)
    paymentdate = models.DateField(db_column='PaymentDate')
    reason = models.TextField(db_column='Reason', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employeebonustable'
        unique_together = (('employee', 'bonus'),)



class Workdaytable(models.Model):
    date = models.DateField(db_column='Date', primary_key=True)
    isworkday = models.IntegerField(db_column='IsWorkday')

    class Meta:
        managed = False
        db_table = 'workdaytable'
