# consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from urllib.parse import parse_qs
import datetime

from api.models import PCInformation
from api.models import StorageTable,MemoryTable,CPUTable,NetworkTable
from django.db import transaction
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async


class SystemInfoConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

        # Extract IP address from query parameters
        query_string = self.scope.get("query_string", b"").decode("utf-8")
        params = parse_qs(query_string)
        ip_address = params.get("ip", [""])[0]

        client = self.scope['client']
        ip = client[0]

        print("This is client",ip)
        print('--------------------------------------------------------------')

        if ip_address:
            await self.channel_layer.group_add(ip_address, self.channel_name)
            # await self.send(json.dumps({"ip":ip_address}))

            # Notify that the user is online

            await self.channel_layer.group_send(
                ip_address,
                {
                    'type': 'user_online',
                    'data': json.dumps({"success":True,"user_id":ip_address}),
                }
            )

    async def disconnect(self, close_code):
        ip_address = self.scope.get('client_addr')
        if ip_address:
            await self.channel_layer.group_discard(ip_address, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        query_string = self.scope.get("query_string", b"").decode("utf-8")
        params = parse_qs(query_string)
        ip_address = params.get("ip", [""])[0]

        # print(ip_address)

        # await self.save_data(data,ip_address)
        await self.channel_layer.group_send(
            ip_address,
            {
                'type': 'SendSystem',
                'data': json.dumps(data)
            }
        )

    async def SendSystem(self,event):
        data = event['data']
        print(data)
        await self.send(text_data=data)

    # async def sendsysteminfo(self, event):
    #     data = event['data']
    #     print(data)
    #     await self.send(text_data=data)

    async def user_online(self, event):
        user_id = event['data']
        print(f"User {user_id} is online.")
        await self.send(text_data=user_id)

    @database_sync_to_async
    def save_data(self,data,ip_address):
            if not PCInformation.objects.filter(ip=ip_address).exists():
                raise Exception("This Pc does not exists")

            time = datetime.datetime.strptime(data['time'],'%H:%M:%S').time()

            with transaction.atomic():
                pc_instance = PCInformation.objects.get(ip=ip_address)
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
