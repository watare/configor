from django.test import TestCase
from ovs_conf.models import Port
VlanMode = Port.VlanMode
from django.test import TestCase
from ovs_conf.models import OvsBridge

class OvsBridgeTestCase(TestCase):
    def setUp(self):
        OvsBridge.objects.create(name='br0', rstp_enable=True, enable_ipv6=True)
        OvsBridge.objects.create(name='br1', rstp_enable=False, enable_ipv6=True)

    def test_str_method(self):
        br0 = OvsBridge.objects.get(name='br0')
        br1 = OvsBridge.objects.get(name='br1')
        self.assertEqual(str(br0), 'br0')
        self.assertEqual(str(br1), 'br1')

    def test_ordering(self):
        bridges = OvsBridge.objects.all()
        self.assertEqual(list(bridges), [
            OvsBridge.objects.get(name='br0'),
            OvsBridge.objects.get(name='br1'),
        ])

// add test for all models

class PortTestCase(TestCase):
    def setUp(self):
        Port.objects.create(name='eth0', vlan_mode=VlanMode.TRUNK, vlan_tag=1)
        Port.objects.create(name='eth1', vlan_mode=VlanMode.TRUNK, vlan_tag=2)

    def test_str_method(self):
        eth0 = Port.objects.get(name='eth0')
        eth1 = Port.objects.get(name='eth1')
        self.assertEqual(str(eth0), 'eth0')
        self.assertEqual(str(eth1), 'eth1')

    def test_ordering(self):
        ports = Port.objects.all()
        self.assertEqual(list(ports), [
            Port.objects.get(name='eth0'),
            Port.objects.get(name='eth1'),
        ])
    def test_save_method(self):
        eth0 = Port.objects.get(name='eth0')
        eth0.save()
        self.assertEqual(eth0.vlan_mode, VlanMode.TRUNK)
        self.assertEqual(eth0.vlan_tag, 1)
        
class VlanModeTestCase(TestCase):
    def test_str_method(self):
        self.assertEqual(str(VlanMode.TRUNK), 'trunk')
        self.assertEqual(str(VlanMode.ACCESS), 'access')
        self.assertEqual(str(VlanMode.NATIVE_TAGGED), 'native-tagged')
        self.assertEqual(str(VlanMode.NATIVE_UNTAGGED), 'native-untagged')
        
class TrunkPortTestCase(TestCase):
    def setUp(self):
        Port.objects.create(name='eth0', vlan_mode=VlanMode.TRUNK, vlan_tag=1)
        Port.objects.create(name='eth1', vlan_mode=VlanMode.TRUNK, vlan_tag=2)
   
    def test_str_method(self):
        eth0 = Port.objects.get(name='eth0')
        eth1 = Port.objects.get(name='eth1')
        self.assertEqual(str(eth0), 'eth0')
        self.assertEqual(str(eth1), 'eth1')

    def test_ordering(self):
        ports = Port.objects.all()
        self.assertEqual(list(ports), [
            Port.objects.get(name='eth0'),
            Port.objects.get(name='eth1'),
        ])
     def save_method(self):
        eth0 = Port.objects.get(name='eth0')
        eth0.save()
        self.assertEqual(eth0.vlan_mode, VlanMode.TRUNK)
        self.assertEqual(eth0.vlan_tag, 1)

        
class OtherPortTestCase(TestCase):
    def setUp(self):
        Port.objects.create(name='eth0', vlan_mode=VlanMode.ACCESS, vlan_tag=1)
        Port.objects.create(name='eth1', vlan_mode=VlanMode.NATIVE_TAGGED, vlan_tag=2)
        Port.objects.create(name='eth2', vlan_mode=VlanMode.NATIVE_UNTAGGED, vlan_tag=3)

    def test_str_method(self):
        eth0 = Port.objects.get(name='eth0')
        eth1 = Port.objects.get(name='eth1')
        eth2 = Port.objects.get(name='eth2')
        self.assertEqual(str(eth0), 'eth0')
        self.assertEqual(str(eth1), 'eth1')
        self.assertEqual(str(eth2), 'eth2')

    def test_ordering(self):
        ports = Port.objects.all()
        self.assertEqual(list(ports), [
            Port.objects.get(name='eth0'),
            Port.objects.get(name='eth1'),
            Port.objects.get(name='eth2'),
        ])
        
    def save_method(self):
        eth0 = Port.objects.get(name='eth0')
        eth0.save()
        self.assertEqual(eth0.vlan_mode, VlanMode.ACCESS)
        self.assertEqual(eth0.vlan_tag, 1)
        
        eth1 = Port.objects.get(name='eth1')
        eth1.save()
        self.assertEqual(eth1.vlan_mode, VlanMode.NATIVE_TAGGED)
        self.assertEqual(eth1.vlan_tag, 2)
        
        eth2 = Port.objects.get(name='eth2')
        eth2.save()
        self.assertEqual(eth2.vlan_mode, VlanMode.NATIVE_UNTAGGED)
        self.assertEqual(eth2.vlan_tag, 3)
        






