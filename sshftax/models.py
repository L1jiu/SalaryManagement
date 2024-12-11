from django.db import models

# Create your models here.
class Employeetable(models.Model):
    employeeid = models.AutoField(db_column='EmployeeID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=6)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employeetable'

class Employeetaxtable(models.Model):
    employeeid = models.IntegerField(db_column='EmployeeID', primary_key=True)  # Field name made lowercase.
    taxname = models.CharField(db_column='TaxName', max_length=100)  # Field name made lowercase.
    taxamount = models.DecimalField(db_column='TaxAmount', max_digits=10, decimal_places=2)  # Field name made lowercase.
    paymentdate = models.DateField(db_column='PaymentDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employeetaxtable'

class Employeesocialsecurityandhousingfundtable(models.Model):
    employeeid = models.IntegerField(db_column='EmployeeID', primary_key=True)  # Field name made lowercase.
    projectname = models.CharField(db_column='ProjectName', max_length=100)  # Field name made lowercase.
    amountdue = models.DecimalField(db_column='AmountDue', max_digits=10, decimal_places=2)  # Field name made lowercase.
    paymentdate = models.DateField(db_column='PaymentDate')  # Field name made lowercase.
    contributionrate = models.DecimalField(db_column='ContributionRate', max_digits=5, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employeesocialsecurityandhousingfundtable'