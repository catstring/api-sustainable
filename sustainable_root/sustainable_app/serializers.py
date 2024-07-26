from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    display_info = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'

    def get_display_info(self, obj):
        return obj.get_display_info()
