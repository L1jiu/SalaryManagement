from rest_framework import serializers
from .models import Employeetable, Performancetable

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employeetable
        fields = '__all__'  # 或者指定字段列表 ['id', 'name', ...]

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performancetable
        fields = '__all__'  # 或者指定字段列表 ['id', 'value', ...]