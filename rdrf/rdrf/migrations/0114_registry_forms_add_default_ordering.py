# Generated by Django 2.1.12 on 2019-11-12 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rdrf', '0113_cde_datatype_and_widget_name_fixup'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registryform',
            options={'ordering': ('registry', 'position')},
        ),
    ]
