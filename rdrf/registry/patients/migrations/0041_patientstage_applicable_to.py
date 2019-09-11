# Generated by Django 2.1.10 on 2019-09-11 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0040_signature_encoding'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientstage',
            name='applicable_to',
            field=models.CharField(blank=True, choices=[('registered', 'Registered patient'), ('consented', 'Consent provided')], max_length=32, null=True),
        ),
    ]
