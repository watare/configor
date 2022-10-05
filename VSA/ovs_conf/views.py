from django.shortcuts import render
from django.http import HttpResponse
from ovs_conf.models import OvsBridge,OtherBridgeConfig,Port,TrunkPort,IpPort,OtherPortConfig
import yaml
from boltons.iterutils import remap

def generate_ovs(request):
    response = HttpResponse(
        content_type='text-plain')
    response['Content-Disposition'] = 'attachment; filename=ovs.txt'
    ovsBridges = OvsBridge.objects.all()
    ovsdic = []
    
    for ovsBridge in ovsBridges:        
        ports = Port.objects.filter(bridge=ovsBridge)
        otherbridgeconfigs = OtherBridgeConfig.objects.filter(bridge=ovsBridge)
        otherbridgedic =  []
        
        for otherbridgeconfig in otherbridgeconfigs:
            otherbridgedic.append(otherbridgeconfig.other_config)
            
        portdic = []
        for port in ports:
            otherportconfigs = OtherPortConfig.objects.filter(port=port)
            ipport = IpPort.objects.filter(port=port) #unused
            trunkports = TrunkPort.objects.filter(port=port)
            trunkdic = []
            otherportconfigdic = []
            
            for otherportconfig in otherportconfigs:
                otherportconfig.append(otherportconfig.other_config)
                
            for trunkport in trunkports:
                trunkdic.append(trunkport.trunk)     
            
            
            portdic.append({'name': port.name,
                            'type': port.type,
                            'interface': port.interface,
                            'tag': port.tag,
                            'trunks': trunkdic,
                           'other_config': otherportconfigdic,
                           })
        ovsdic.append({'name': ovsBridge.name,
                       'rstp_enable': ovsBridge.rstp_enable,
                       'enable_ipv6' :ovsBridge.enable_ipv6,
                       'other_config' : otherbridgedic,
                       'ports': portdic
                       })
        print(ovsdic)
        
        drop_falsey = lambda path, key, value: bool(value)
        ovsdiccleaned = remap(ovsdic, visit=drop_falsey)
        ovs_conf = yaml.dump(ovsdiccleaned,sort_keys=False)
        #lines.append(f'{ports[0].name}\n')

    response.writelines(ovs_conf)
    return response