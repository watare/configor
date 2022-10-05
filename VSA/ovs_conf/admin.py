from django.contrib import admin
from ovs_conf.models import OvsBridge,OtherBridgeConfig,Port,TrunkPort,IpPort,OtherPortConfig

class OtherBridgeConfigAdmin(admin.ModelAdmin):
    list_display = ('bridge','other_config')
    
class OtherPortConfigAdmin(admin.ModelAdmin):
    list_display = ('port','other_config')
    
class PortAdmin(admin.ModelAdmin):
    list_display = ('name','bridge','type','vlan_mode')
    
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