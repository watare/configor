from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class OvsBridge(models.Model):
    
    def __str__(self) -> str:
        return f'{self.name}'
    name = models.fields.CharField(max_length=50)
    rstp_enable = models.fields.BooleanField(default=False)
    enable_ipv6 = models.fields.BooleanField(default=False)

class OtherBridgeConfig(models.Model):
    
    def __str__(self) -> str:
        return f'{self.other_config}'
    other_config = models.fields.CharField(max_length=50)
    bridge = models.ForeignKey(OvsBridge,null=True,on_delete=models.CASCADE)
    
class Port(models.Model):
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    bridge = models.ForeignKey(OvsBridge,null=True,on_delete=models.CASCADE)
    name = models.fields.CharField(max_length=50) #the interface bridge name
    
    class Type(models.TextChoices):
        internal = 'internal'
        system = 'system'
        dpdk = 'dpdk'
        dpdkvhostuserclient = 'dpdkvhostuserclient'
        tap = "tap"
        vxlan = "vxlan"
    type = models.fields.CharField(choices=Type.choices,max_length=20)
    
    interface = models.fields.CharField(blank=True, default='',max_length=100)
    tag = models.fields.IntegerField(blank=True,null=True,
        validators=[MinValueValidator(0),MaxValueValidator(4095)]
    )
    
    class VlanMode(models.TextChoices):
    # le _ doit être remplacé par un - lors de la génération du fichier yaml
        access = 'access'
        native_tagged = 'native-tagged'
        native_untagged = 'native-untagged'
        trunk = 'trunk'
    vlan_mode = models.fields.CharField(choices=VlanMode.choices,max_length=15)

    mac = models.fields.CharField(blank=True, default='',max_length=100)
    remote_ip = models.fields.CharField(blank=True,max_length=100, default='')
    remote_port = models.fields.IntegerField(default=4789)
    key = models.fields.IntegerField(blank=True,null=True) # vxlan_key
    ingress_policy_rate = models.fields.IntegerField(blank=True,null=True) #The maximum rate (in Kbps) that this port should be allowed
    #to send.If not set, this policy will be disabled
    active = models.fields.BooleanField(default=True) #A parameter to the policing algorithm to indicate 
    ingress_policing_burst = models.fields.IntegerField(blank=True,null=True) #the maximum amount of data (in Kb) that
     #this interface can send beyond the policing rate.If not set, this policy will be disabled.
