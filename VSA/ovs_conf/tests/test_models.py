from django.test import TestCase
from myapp.models import VlanMode

class VlanModeModelTest(TestCase):
    def test_vlan_mode_model(self):
        # Create a VlanMode instance
        vlan_mode = VlanMode(vlan_mode=VlanMode.access)

        # Save the instance to the database
        vlan_mode.save()

        # Check that the instance was saved to the database
        saved_vlan_mode = VlanMode.objects.first()
        self.assertEqual(saved_vlan_mode, vlan_mode)
from django.test import TestCase
from myapp.models import VlanMode

class VlanModeModelTest(TestCase):
    def test_vlan_mode_model(self):
        # Create a VlanMode instance
        vlan_mode = VlanMode(vlan_mode=VlanMode.access)

        # Save the instance to the database
        vlan_mode.save()

        # Check that the instance was saved to the database
        saved_vlan_mode = VlanMode.objects.first()
        self.assertEqual(saved_vlan_mode, vlan_mode)
def test_vlan_mode_field_choices(self):
    # Create a VlanMode instance with each of the choices
    vlan_mode_access = VlanMode(vlan_mode=VlanMode.access)
    vlan_mode_native_tagged = VlanMode(vlan_mode=VlanMode.native_tagged)
    vlan_mode_native_untagged = VlanMode(vlan_mode=VlanMode.native_untagged)
    vlan_mode_trunk = VlanMode(vlan_mode=VlanMode.trunk)

    # Save the instances to the database
    vlan_mode_access.save()
    vlan_mode_native_tagged.save()
    vlan_mode_native_untagged.save()
    vlan_mode_trunk.save()

    # Check that the vlan_mode field has the correct choices
    self.assertEqual(vlan_mode_access.vlan_mode, VlanMode.access)
    self.assertEqual(vlan_mode_native_tagged.vlan_mode, VlanMode.native_tagged)
    self.assertEqual(vlan_mode_native_untagged.vlan_mode, VlanMode.native_untagged)
    self.assertEqual(vlan_mode_trunk.vlan_mode, VlanMode.trunk)
def test_mac_field_is_optional(self):
    # Create a VlanMode instance without a mac
    vlan_mode = VlanMode(vlan_mode=VlanMode.access)

    # Save the instance to the database
    vlan_mode.save()

    # Check that the instance was saved to the database
    saved_vlan_mode = VlanMode.objects.first()
    self.assertEqual(saved_vlan_mode, vlan_mode)
def test_mac_field_is_optional(self):
    # Create a VlanMode instance without a mac
    vlan_mode = VlanMode(vlan_mode=VlanMode.access)

    # Save the instance to the database
    vlan_mode.save()

    # Check that the instance was saved to the database
    saved_vlan_mode = VlanMode.objects.first()
    self.assertEqual(saved_vlan_mode, vlan_mode)
