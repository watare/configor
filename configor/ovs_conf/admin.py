from django.contrib import admin
from ovs_conf.models import OvsBridge,OtherBridgeConfig,Port,TrunkPort,IpPort,OtherPortConfig
from ovs_conf.models import DomainVm,MemoryVm,SubEleModel

class OtherBridgeConfigAdmin(admin.ModelAdmin):
    list_display = ('bridge','other_config')
    
class OtherPortConfigAdmin(admin.ModelAdmin):
    list_display = ('port','other_config')
    
class PortAdmin(admin.ModelAdmin):
    list_display = ('id','name','bridge','type','vlan_mode')
    
class TrunkAdmin(admin.ModelAdmin):
    list_display = ('id','port','trunk')
    
class IpAdmin(admin.ModelAdmin):
    list_display = ('id','port','ip')
    
admin.site.register(OvsBridge)
admin.site.register(OtherBridgeConfig,OtherBridgeConfigAdmin)
admin.site.register(Port,PortAdmin)
admin.site.register(TrunkPort,TrunkAdmin)
admin.site.register(IpPort,IpAdmin)
admin.site.register(OtherPortConfig,OtherPortConfigAdmin)


# VM admin
class DomainVmAdmin(admin.ModelAdmin):
    list_display = ('id','attr_type','text_name')

class MemoryVmAdmin(admin.ModelAdmin):
    list_display = ('id','text_memory')  
 
class SubEleAdmin(admin.ModelAdmin):
    list_display = ('id','name','fkey','text','attributes') 
         
admin.site.register(DomainVm,DomainVmAdmin)
admin.site.register(MemoryVm,MemoryVmAdmin)
admin.site.register(SubEleModel,SubEleAdmin)
    