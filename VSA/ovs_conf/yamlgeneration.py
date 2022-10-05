from django.db import models
from ovs_conf.models import OvsBridge,OtherBridgeConfig,Port,TrunkPort,IpPort,OtherPortConfig

bridges = OvsBridges.objects.all()
print(bridges)