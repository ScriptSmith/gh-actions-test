# Generated by Django 2.1.12 on 2019-11-19 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdrf', '0115_form_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='rdrfcontext',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]