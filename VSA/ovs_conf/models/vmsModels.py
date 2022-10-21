from django.db import models
from ovs_conf.models.ovsModels import Port
from django.core.validators import MaxValueValidator, MinValueValidator
class Vm(models.Model):
    
    def __str__(self) -> str:
        return f'{self.name}'
    ordering = ("name", )
    name = models.fields.CharField(max_length=50)
    mac = models.fields.CharField(max_length=50)
    interface = models.ForeignKey(Port,on_delete=models.CASCADE)
    pci = models.fields.CharField(max_length=50)
    
    class Meta:
        ordering = ['name']
    
class DomainVm(models.Model):
    
    def __str__(self) -> str:
        return f'{self.name}'
    attr_type = models.fields.CharField(max_length=5)
    text_name = models.fields.CharField(max_length=20)
        
    class Meta:
        ordering = ['text_name']

class MetaVm(models.Model):
    
    vm = models.ForeignKey(DomainVm,on_delete=models.CASCADE)
    
class MemoryVm(models.Model):
    
    vm = models.ForeignKey(DomainVm,on_delete=models.CASCADE)
    attr_unit = "KiB"
    text_memory = models.fields.IntegerField(
        validators=[MinValueValidator(1000),MaxValueValidator(10000)]
    )

    #faire un modele par type d'élément. 
    #lui assosicer la bonne foreing key
    #remplir manuellement quelque champs
    #faire une fonction qui reconstruit l'arborescence (en partant des éléments les plus bas)