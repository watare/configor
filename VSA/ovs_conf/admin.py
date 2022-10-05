from django.contrib import admin
from ovs_conf.models import OvsBridge,OtherBridgeConfig,Port

class OtherConfig(admin.ModelAdmin):
    list_display = ('bridge','other_config')
class PortAdmin(admin.ModelAdmin):
    list_display = ('name','bridge','type','vlan_mode')
    
admin.site.register(OvsBridge)
admin.site.register(OtherBridgeConfig,OtherConfig)
admin.site.register(Port,PortAdmin)