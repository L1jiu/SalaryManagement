# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Attendancetable(models.Model):
    recordid = models.AutoField(db_column='RecordID', primary_key=True)  # Field name made lowercase. The composite primary key (RecordID, EmployeeID, Date) found, that is not supported. The first column is selected.
    employeeid = models.ForeignKey('Employeetable', models.DO_NOTHING, db_column='EmployeeID')  # Field name made lowercase.
    date = models.ForeignKey('Workdaytable', models.DO_NOTHING, db_column='Date')  # Field name made lowercase.
    clockintime = models.TimeField(db_column='ClockInTime', blank=True, null=True)  # Field name made lowercase.
    clockouttime = models.TimeField(db_column='ClockOutTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'attendancetable'
        unique_together = (('recordid', 'employeeid', 'date'),)


class Bonustable(models.Model):
    bonusid = models.AutoField(db_column='BonusID', primary_key=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2)  # Field name made lowercase.
    paymentdate = models.DateField(db_column='PaymentDate')  # Field name made lowercase.
    reason = models.TextField(db_column='Reason', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bonustable'


class Employeebonustable(models.Model):
    employeeid = models.IntegerField(db_column='EmployeeID', primary_key=True)  # Field name made lowercase. The composite primary key (EmployeeID, BonusID) found, that is not supported. The first column is selected.
    bonusid = models.ForeignKey(Bonustable, models.DO_NOTHING, db_column='BonusID')  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2)  # Field name made lowercase.
    paymentdate = models.DateField(db_column='PaymentDate')  # Field name made lowercase.
    reason = models.TextField(db_column='Reason', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employeebonustable'
        unique_together = (('employeeid', 'bonusid'),)


class Employeepositiontable(models.Model):
    employeeid = models.OneToOneField('Employeetable', models.DO_NOTHING, db_column='EmployeeID', primary_key=True)  # Field name made lowercase. The composite primary key (EmployeeID, PositionName) found, that is not supported. The first column is selected.
    positionname = models.ForeignKey('Positiontable', models.DO_NOTHING, db_column='PositionName')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employeepositiontable'
        unique_together = (('employeeid', 'positionname'),)


class Employeesocialsecurityandhousingfundtable(models.Model):
    employeeid = models.OneToOneField('Employeetable', models.DO_NOTHING, db_column='EmployeeID', primary_key=True)  # Field name made lowercase. The composite primary key (EmployeeID, ProjectName, PaymentDate) found, that is not supported. The first column is selected.
    projectname = models.ForeignKey('Socialsecurityandhousingfundtable', models.DO_NOTHING, db_column='ProjectName')  # Field name made lowercase.
    amountdue = models.DecimalField(db_column='AmountDue', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    paymentdate = models.ForeignKey('Workdaytable', models.DO_NOTHING, db_column='PaymentDate')  # Field name made lowercase.
    contributionrate = models.ForeignKey('Socialsecurityandhousingfundtable', models.DO_NOTHING, db_column='ContributionRate', to_field='ContributionRate', related_name='employeesocialsecurityandhousingfundtable_contributionrate_set')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employeesocialsecurityandhousingfundtable'
        unique_together = (('employeeid', 'projectname', 'paymentdate'),)


class Employeetable(models.Model):
    employeeid = models.AutoField(db_column='EmployeeID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=6)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employeetable'


class Employeetaxtable(models.Model):
    employeeid = models.OneToOneField(Employeetable, models.DO_NOTHING, db_column='EmployeeID', primary_key=True)  # Field name made lowercase. The composite primary key (EmployeeID, TaxName, PaymentDate) found, that is not supported. The first column is selected.
    taxname = models.ForeignKey('Taxtable', models.DO_NOTHING, db_column='TaxName')  # Field name made lowercase.
    taxamount = models.DecimalField(db_column='TaxAmount', max_digits=10, decimal_places=2)  # Field name made lowercase.
    paymentdate = models.ForeignKey('Workdaytable', models.DO_NOTHING, db_column='PaymentDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employeetaxtable'
        unique_together = (('employeeid', 'taxname', 'paymentdate'),)


class Grosssalary(models.Model):
    employeeid = models.OneToOneField(Employeetable, models.DO_NOTHING, db_column='EmployeeID', primary_key=True)  # Field name made lowercase. The composite primary key (EmployeeID, Year, Month) found, that is not supported. The first column is selected.
    year = models.IntegerField(db_column='Year')  # Field name made lowercase.
    month = models.IntegerField(db_column='Month')  # Field name made lowercase.
    basesalary = models.ForeignKey('Positiontable', models.DO_NOTHING, db_column='BaseSalary', to_field='BaseSalary', blank=True, null=True)  # Field name made lowercase.
    absentdeduction = models.DecimalField(db_column='AbsentDeduction', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    overtimepay = models.DecimalField(db_column='OvertimePay', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    performancebonus = models.DecimalField(db_column='PerformanceBonus', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    yearendbonus = models.DecimalField(db_column='YearEndBonus', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'grosssalary'
        unique_together = (('employeeid', 'year', 'month'),)


class Performanceevaluationtable(models.Model):
    employeeid = models.IntegerField(db_column='EmployeeID', primary_key=True)  # Field name made lowercase. The composite primary key (EmployeeID, IndicatorName, EvaluationDate) found, that is not supported. The first column is selected.
    indicatorname = models.ForeignKey('Performancetable', models.DO_NOTHING, db_column='IndicatorName')  # Field name made lowercase.
    score = models.DecimalField(db_column='Score', max_digits=5, decimal_places=2)  # Field name made lowercase.
    evaluationdate = models.DateField(db_column='EvaluationDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'performanceevaluationtable'
        unique_together = (('employeeid', 'indicatorname', 'evaluationdate'),)


class Performancetable(models.Model):
    indicatorname = models.CharField(db_column='IndicatorName', primary_key=True, max_length=100)  # Field name made lowercase.
    weight = models.DecimalField(db_column='Weight', max_digits=5, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'performancetable'


class Positiontable(models.Model):
    positionname = models.CharField(db_column='PositionName', primary_key=True, max_length=100)  # Field name made lowercase.
    basesalary = models.DecimalField(db_column='BaseSalary', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'positiontable'


class Socialsecurityandhousingfundtable(models.Model):
    projectname = models.CharField(db_column='ProjectName', primary_key=True, max_length=100)  # Field name made lowercase.
    contributionrate = models.DecimalField(db_column='ContributionRate', max_digits=5, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'socialsecurityandhousingfundtable'


class Taxtable(models.Model):
    taxname = models.CharField(db_column='TaxName', primary_key=True, max_length=100)  # Field name made lowercase.
    lowerlimit = models.DecimalField(db_column='LowerLimit', max_digits=10, decimal_places=2)  # Field name made lowercase.
    upperlimit = models.DecimalField(db_column='UpperLimit', max_digits=10, decimal_places=2)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=5, decimal_places=2)  # Field name made lowercase.
    quickdeduction = models.DecimalField(db_column='QuickDeduction', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'taxtable'


class Workdaytable(models.Model):
    date = models.DateField(db_column='Date', primary_key=True)  # Field name made lowercase.
    isworkday = models.IntegerField(db_column='IsWorkday')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'workdaytable'
