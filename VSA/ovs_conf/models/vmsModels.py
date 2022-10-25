from unicodedata import name
from django.db import models
from ovs_conf.models.ovsModels import OvsBridge, Port
from django.core.validators import MaxValueValidator, MinValueValidator

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
    
class SubEleManager(models.Manager):
    def createSub(self,subname,parent=None,text=None,**kwargs):
    # def createSub(self,name):        
        subele = self.create(name=subname)
        subele.fkey = parent
        if len(kwargs) > 0:
            subele.attributes = {}
        for k,v in kwargs.items():
            # print("%s = %s" % (k, v))
            subele.attributes[k] = v
        if not text == None:
            subele.text = text
        

        # do something with the book
        return subele
class SubEleModel(models.Model):
   #classe permettant de sauvegarder en database tous les elements du formulaire 
    name = models.CharField(max_length=100)
    fkey = models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True)
    text = models.CharField(max_length=100)
    attributes = models.TextField(blank=True, null=True, default='{}')
    objects = SubEleManager()
    
    class Meta:
        ordering = ['name']
    

    #faire un modele par type d'élément. 
    #lui assosicer la bonne foreing key
    #remplir manuellement quelque champs
    #faire une fonction qui reconstruit l'arborescence (en partant des éléments les plus bas)