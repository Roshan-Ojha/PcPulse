from rest_framework import serializers
from django.core.validators import validate_ipv46_address

class PcInfoSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    hostname = serializers.CharField(required=True)
    ip = serializers.CharField(validators=[validate_ipv46_address])


class SystemInfoSerializer(serializers.Serializer):
    total_storage = serializers.CharField(required=True)
    used_storage = serializers.CharField(required=True)
    free_storage = serializers.CharField(required=True)
    total_memory = serializers.CharField(required=True)
    used_memory = serializers.CharField(required=True)
    free_memory = serializers.CharField(required=True)
    uptime = serializers.CharField(required=True)
    cpu_usage = serializers.CharField(required=True)
    upload = serializers.CharField(required=True)
    download = serializers.CharField(required=True)
    time = serializers.CharField(required=True)
