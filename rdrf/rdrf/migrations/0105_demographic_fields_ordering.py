# Generated by Django 2.1.10 on 2019-08-12 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rdrf', '0104_demographic_fields_remove_hidden_and_readonly'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='demographicfields',
            options={'ordering': ('registry', '-is_section', 'field', 'status'), 'verbose_name_plural': 'Demographic Fields'},
        ),
    ]
