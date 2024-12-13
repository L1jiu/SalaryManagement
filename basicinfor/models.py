from django.db import models

# Create your models here.

class Employeetable(models.Model):
    employeeid = models.AutoField(db_column='EmployeeID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=6)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=20, blank=True, null=True)  # Field name made lowercase.

    @property
    def position(self):
        try:
            return self.employeepositiontable_set.get().positionname
        except Employeepositiontable.DoesNotExist:
            return None

    class Meta:
        managed = False
        db_table = 'employeetable'

class Positiontable(models.Model):
    positionname = models.CharField(db_column='PositionName', primary_key=True, max_length=100)  # Field name made lowercase.
    basesalary = models.DecimalField(db_column='BaseSalary', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'positiontable'

    def __str__(self):
        return self.positionname  # 返回职位名称作为对象的字符串表示

class Employeepositiontable(models.Model):
    employeeid = models.OneToOneField('Employeetable', models.DO_NOTHING, db_column='EmployeeID', primary_key=True)  # Field name made lowercase. The composite primary key (EmployeeID, PositionName) found, that is not supported. The first column is selected.
    positionname = models.ForeignKey('Positiontable', models.DO_NOTHING, db_column='PositionName')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employeepositiontable'
        unique_together = (('employeeid', 'positionname'),)