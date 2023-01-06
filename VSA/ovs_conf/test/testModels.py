from django.test import TestCase
from ovs_conf.models import Port
VlanMode = Port.VlanMode
from django.test import TestCase
from ovs_conf.models import OvsBridge
#commentaires
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
