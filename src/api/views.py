from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny

from django.db import transaction

import datetime

from api.models import PCInformation
from api.models import StorageTable,MemoryTable,CPUTable,NetworkTable

from api import serializers

# Create your views here.

class PCInfoAPI(APIView):
    
    permission_classes = [AllowAny]
    pc_serializer = serializers.PcInfoSerializer

    def post(self,request):
        try:
            pc_serializer = self.pc_serializer(data=request.data)
            pc_serializer.is_valid(raise_exception=True)
            data = pc_serializer.validated_data

            if not PCInformation.objects.filter(ip=data.get('ip')).exists():
                pcinfo_instance = PCInformation.objects.create(
                    username = data.get('username'),
                    hostname = data.get('hostname'),
                    ip = data.get('ip')
                )
                pcinfo_instance.save()

            return Response({"success":True})
        except Exception as e:
            return Response({"success":False,"message":str(e)})
        
    
    def get (self, request):
        try:
            pcinfo_instance = PCInformation.objects.all()

            data = [{
                "username":info.username,
                "hostname":info.hostname,
                "ip":info.ip
                } for info in pcinfo_instance]
            return Response({"success":True,"data":data})
        except Exception as e:
            return Response({"success":False, "message":str(e)})


class SystemInfoAPI(APIView):
    permission_classes=[AllowAny]
    system_serializer = serializers.SystemInfoSerializer
    def post(self,request): 
        try:
            ip = request.query_params.get('ip')
            
            system_info_serializer = self.system_serializer(data=request.data)
            system_info_serializer.is_valid(raise_exception=True)
            data = system_info_serializer.validated_data
        
            if not PCInformation.objects.filter(ip=ip).exists():
                raise Exception("This Pc does not exists")
            
            time = datetime.datetime.strptime(data['time'],'%H:%M:%S').time()
            
            with transaction.atomic():
                pc_instance = PCInformation.objects.get(ip=ip)

                storage_instance = StorageTable.objects.create(
                    pc = pc_instance,
                    total_storage = data['total_storage'],
                    used_storage = data['used_storage'],
                    free_storage = data['free_storage'],
                    time=time
                )
                storage_instance.save()
                memory_instance = MemoryTable.objects.create(
                    pc = pc_instance,
                    total_memory = data['total_memory'],
                    used_memory = data['used_memory'],
                    free_memory = data['free_memory'],
                    time=time
                )
                memory_instance.save()

                print("here")
                cpu_instance = CPUTable.objects.create(
                    pc=pc_instance,
                    uptime = data['uptime'],
                    cpu_usage = data['cpu_usage'],
                    time=time
                )
                cpu_instance.save()


                network_instance = NetworkTable.objects.create(
                    pc=pc_instance,
                    upload = data['upload'],
                    download = data['download'],
                    time = data['time']
                )
                network_instance.save()



            return Response({"success":True})
        except Exception as e:
            return Response({"success":False,"message":str(e)})
        
    
    def get(self,request):
        try:
            if not request.query_params.keys() not in ["ip","resource"]:
                raise Exception("Invalid method")

            ip = request.query_params.get('ip')
            resource = request.query_params.get('resource')

            if not resource in ["storage","memory","cpu","network"]:
                raise Exception("This resource info does not exists")
            
            if not PCInformation.objects.filter(ip=ip).exists():
                raise Exception("This Pc does not exists")
            
            pc_instance = PCInformation.objects.get(ip=ip)

            if resource == 'storage':
                data = [{
                    "total":storage.total_storage,
                    "used":storage.used_storage,
                    "free":storage.free_storage,
                    "time":storage.time,
                    "date":storage.date
                }for storage in StorageTable.objects.filter(pc=pc_instance)]
            
            if resource == 'memory':
                data = [{
                    "total":memory.total_memory,
                    "used":memory.used_memory,
                    "free":memory.free_memory,
                    "time":memory.time,
                    "date":memory.date
                }for memory in MemoryTable.objects.filter(pc=pc_instance)]

            if resource == 'cpu':
                data = [{
                    "uptime":cpu.uptime,
                    "usage":cpu.cpu_usage,
                    "time":cpu.time,
                    "date":cpu.date
                }for cpu in CPUTable.objects.filter(pc=pc_instance)]

            if resource == "network":
                data = [{
                    "upload":network.upload,
                    "download":network.download,
                    "time":network.time,
                    "date":network.date
                }for network in NetworkTable.objects.filter(pc=pc_instance)]

            return Response({"success":True,"data":data})
        except Exception as e:
            return Response({"success":False,"message":str(e)})