# Generated by Django 2.1.10 on 2019-08-02 03:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rdrf', '0099_m2m_groups_data_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demographicfields',
            name='group',
        ),
    ]