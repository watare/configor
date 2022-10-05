# Generated by Django 4.1.2 on 2022-10-05 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ovs_conf", "0007_alter_port_key"),
    ]

    operations = [
        migrations.AlterField(
            model_name="port",
            name="type",
            field=models.CharField(
                choices=[
                    ("internal", "Internal"),
                    ("system", "System"),
                    ("dpdk", "Dpdk"),
                    ("dpdkvhostuserclient", "Dpdkvhostuserclient"),
                    ("tap", "Tap"),
                    ("vxlan", "Vxlan"),
                ],
                max_length=20,
            ),
        ),
    ]
