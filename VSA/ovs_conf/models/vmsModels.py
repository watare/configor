from django.db import models
from ovs_conf.models.ovsModels import Port
class Vm(models.Model):
    
    def __str__(self) -> str:
        return f'{self.name}'
    ordering = ("name", )
    name = models.fields.CharField(max_length=50)
    mac = models.fields.CharField(max_length=50)
    interface = models.ForeignKey(Port,on_delete=models.CASCADE)
    pci = models.fields.CharField(max_length=50)