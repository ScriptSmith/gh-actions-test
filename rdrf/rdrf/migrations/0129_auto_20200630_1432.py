# Generated by Django 2.2.13 on 2020-06-30 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rdrf', '0128_cdefile_set_mime_type_data_migration'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Annotation',
        ),
        migrations.AddField(
            model_name='survey',
            name='context_form_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rdrf.ContextFormGroup'),
        ),
        migrations.AddField(
            model_name='survey',
            name='form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rdrf.RegistryForm'),
        ),
        migrations.AddField(
            model_name='surveyquestion',
            name='cde_path',
            field=models.CharField(blank=True, help_text='Format: <i>/[form_name]/[section_code]/</i><br/>Example: <i>/BaselineTreatmentForm/BASELINETREATMENT/</i>', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='emailnotification',
            name='description',
            field=models.CharField(choices=[('account-locked', 'Account Locked'), ('other-clinician', 'Other Clinician'), ('new-patient', 'New Patient Registered'), ('new-patient-parent', 'New Patient Registered (Parent)'), ('account-verified', 'Account Verified'), ('password-expiry-warning', 'Password Expiry Warning'), ('reminder', 'Reminder'), ('clinician-signup-request', 'Clinician Signup Request'), ('clinician-activation', 'Clinician Activation'), ('clinician-selected', 'Clinician Selected'), ('participant-clinician-notification', 'Participant Clinician Notification'), ('patient-consent-change', 'Patient Consent Change'), ('new-carer', 'Primary Caregiver Registered'), ('carer-invited', 'Primary Caregiver Invited'), ('carer-assigned', 'Primary Caregiver Assigned'), ('carer-activated', 'Primary Caregiver Activated'), ('carer-deactivated', 'Primary Caregiver Deactivated'), ('survey-request', 'Survey Request')], max_length=100),
        ),
    ]
