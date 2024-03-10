from django.db import models

# Create your models here.


class PCInformation(models.Model):
    username = models.CharField(max_length=255)
    hostname = models.CharField(max_length = 255)
    ip = models.GenericIPAddressField()

    def __str__(self):
        return self.username
    

class StorageTable(models.Model):
    pc = models.ForeignKey(PCInformation, on_delete = models.CASCADE)
    total_storage = models.CharField(max_length = 255)
    used_storage = models.CharField(max_length = 255)
    free_storage = models.CharField(max_length=255)
    time = models.TimeField()
    date  = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.pc.username
    

class MemoryTable(models.Model):
    pc = models.ForeignKey(PCInformation, on_delete = models.CASCADE)
    total_memory = models.CharField(max_length = 255)
    used_memory = models.CharField(max_length = 255)
    free_memory = models.CharField(max_length=255)
    time = models.TimeField()
    date  = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.pc.username
    

class CPUTable(models.Model):
    pc = models.ForeignKey(PCInformation, on_delete = models.CASCADE)
    uptime = models.CharField(max_length=255)
    cpu_usage = models.CharField(max_length=255)
    time = models.TimeField()
    date  = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.pc.username
    
class NetworkTable(models.Model):
    pc = models.ForeignKey(PCInformation, on_delete = models.CASCADE)
    upload=models.CharField(max_length=255)
    download = models.CharField(max_length = 255)
    time = models.TimeField()
    date  = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.pc.username