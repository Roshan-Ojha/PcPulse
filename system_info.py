import psutil
import time
from datetime import timedelta,datetime
# import datetime
import getpass
import socket
import requests
import concurrent.futures
import asyncio
import websockets
import json

#Storage Information
def storage_info():
    time.sleep(1)



 
    disk_usage = psutil.disk_usage('/')
    total_storage = round(disk_usage.total / (2**30) ,2 ) #GB
    used_storage = round(disk_usage.used / (2**30), 2)     #GB
    free_storage = round(disk_usage.free/(2**30),2  )    #GB

    return({
        "total_storage":total_storage,
        "used_storage":used_storage,
        "free_storage":free_storage,
    })

# print(total_storage,uses_storage,free_storage)


# Memory Information
def memory_info():
    time.sleep(1)
    times = datetime.now()
    current_time = f"{times.hour}: {times.minute}: {times.second}"

    memory_usage = psutil.virtual_memory()
    total_memory = round(memory_usage.total / (2**20), 2)  # MB
    used_memory = round(memory_usage.used / (2**20), 2)    # MB
    free_memory = round(memory_usage.free / (2**20), 2)   # MB
    
    return({
        "total_memory":total_memory,
        "used_memory":used_memory,
        "free_memory":free_memory,

    })

# print(total_memory,used_memory,free_memory)

#CPU Information
def cpu_info():
    boot_time = datetime.fromtimestamp(psutil.boot_time())  # Convert boot time to datetime
    current_time = datetime.now()
    elasped_time = current_time - boot_time

    seconds = elasped_time.seconds
    hours=seconds // 3600
    minutes=(seconds%3600)//60
    sec = seconds%60
    uptime = f"{hours}:{minutes}:{sec}"
    

    cpu_usage = psutil.cpu_percent(interval=1)




    return({
        "uptime":uptime,
        "cpu_usage":cpu_usage,
   
   
    })

# print(uptime,cpu_usage,idle_cpu_time)


#Network Information
def network_info():
    

    bytes_send_first = psutil.net_io_counters().bytes_sent
    bytes_received_first = psutil.net_io_counters().bytes_recv
    time.sleep(1)
    bytes_send_second = psutil.net_io_counters().bytes_sent
    bytes_received_second = psutil.net_io_counters().bytes_recv
    
    upload_speed = round((bytes_send_second-bytes_send_first)/1024,2)
    download_speed = round((bytes_received_second-bytes_received_first)/1024,2)

    return({
        "upload":upload_speed,
        "download":download_speed,

    })

# print(round(bytes_send/(2**30),2),round(bytes_received/(2**30),2))


#PC information
def pc_info():
    username= getpass.getuser()
    hostname = socket.gethostname()
    # ip = socket.gethostbyname_ex(hostname)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    # print(s.getsockname())
    ip = s.getsockname()[0]

    return {"username":username,
            "hostname":hostname,
            "ip":ip}

 
def send_pc_info():
    pc_data = pc_info()
    response = requests.post('http://192.168.1.87:8000/api/v1/pcinfo/',json=pc_data)

    if response.status_code == 200:
        print(response.json())
    else:
        try:
            # Attempt to print JSON error message if possible
            error_data = response.json()
            print(f"Error: {error_data['message']}")  # Assuming the error has a 'message' key
        except (ValueError, KeyError):
            # Handle cases where the response isn't valid JSON
            print(f"Error: {response.status_code} - {response.text}")



async def send_system_info(storage_information,memory_information,cpu_information,network_information):
    times = datetime.now()
    current_time = f"{times.hour}:{times.minute}:{times.second}"
    system_info = {**storage_information.result(),**memory_information.result(),**cpu_information.result(),**network_information.result()}
    system_info["time"] = current_time
    system_info["ip"] = pc_info()["ip"]
    system_info["user"] = pc_info()["username"]
    system_info["host"] = pc_info()["hostname"]

    await websocket.send(json.dumps(system_info))
        # response = await websocket.recv()

    response = await websocket.recv()
    print(response)

# asyncio.get_event_loop().run_until_complete(send_system_info())

if __name__ == "__main__":
    send_pc_info()
    ip = pc_info()["ip"]
    uri = f"ws://192.168.1.87:8000/ws/system_info/?ip={ip}"
    websocket = asyncio.get_event_loop().run_until_complete(websockets.connect(uri))

    while True:
        with concurrent.futures.ThreadPoolExecutor() as executer:
            storage_information = executer.submit(storage_info)
            memory_information = executer.submit(memory_info)
            cpu_information = executer.submit(cpu_info)
            network_information = executer.submit(network_info)
            print(pc_info())

            executer.submit(send_system_info,storage_information,memory_information,cpu_information,network_information)
            asyncio.get_event_loop().run_until_complete(send_system_info(storage_information,memory_information,cpu_information,network_information))

    

