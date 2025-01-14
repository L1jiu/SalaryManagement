# Generated by Django 5.0.3 on 2024-12-11 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employeesocialsecurityandhousingfundtable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employeeid', models.IntegerField(db_column='EmployeeID')),
                ('projectname', models.CharField(db_column='ProjectName', max_length=100)),
                ('amountdue', models.DecimalField(db_column='AmountDue', decimal_places=2, max_digits=10)),
                ('paymentdate', models.DateField(db_column='PaymentDate')),
                ('contributionrate', models.DecimalField(db_column='ContributionRate', decimal_places=2, max_digits=5)),
            ],
            options={
                'db_table': 'employeesocialsecurityandhousingfundtable',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Employeetable',
            fields=[
                ('employeeid', models.AutoField(db_column='EmployeeID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=100)),
                ('gender', models.CharField(db_column='Gender', max_length=6)),
                ('phonenumber', models.CharField(blank=True, db_column='PhoneNumber', max_length=20, null=True)),
            ],
            options={
                'db_table': 'employeetable',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Employeetaxtable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employeeid', models.IntegerField(db_column='EmployeeID')),
                ('taxname', models.CharField(db_column='TaxName', max_length=100)),
                ('taxamount', models.DecimalField(db_column='TaxAmount', decimal_places=2, max_digits=10)),
                ('paymentdate', models.DateField(db_column='PaymentDate')),
            ],
            options={
                'db_table': 'employeetaxtable',
                'managed': False,
            },
        ),
    ]
