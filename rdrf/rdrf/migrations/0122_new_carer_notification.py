# Generated by Django 2.2.10 on 2020-02-26 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdrf', '0121_cde_add_email_datatype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailnotification',
            name='description',
            field=models.CharField(choices=[('account-locked', 'Account Locked'), ('other-clinician', 'Other Clinician'), ('new-patient', 'New Patient Registered'), ('new-patient-parent', 'New Patient Registered (Parent)'), ('account-verified', 'Account Verified'), ('password-expiry-warning', 'Password Expiry Warning'), ('reminder', 'Reminder'), ('clinician-signup-request', 'Clinician Signup Request'), ('clinician-activation', 'Clinician Activation'), ('clinician-selected', 'Clinician Selected'), ('participant-clinician-notification', 'Participant Clinician Notification'), ('patient-consent-change', 'Patient Consent Change'), ('new-carer', 'Patient Carer Registered'), ('carer-invited', 'Patient Carer Invited'), ('carer-assigned', 'Patient Carer Assigned'), ('carer-activated', 'Patient Carer Activated'), ('carer-deactivated', 'Patient Carer Deactivated')], max_length=100),
        ),
    ]
