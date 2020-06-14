# Generated by Django 2.2.10 on 2020-05-05 12:18

import logging
import magic

from django.db import migrations, models
from rdrf.db import filestorage

logger = logging.getLogger(__name__)


def set_mime_type(apps, schema_editor):
    CDEFile = apps.get_model('rdrf', 'CDEFile')
    to_update = CDEFile.objects.filter(mime_type__isnull=True).values_list('id', 'filename')
    logger.info(f"Setting mime_type for {to_update.count()} record(s)")
    for file_id, file_name in to_update:
        try:
            file_info = filestorage.get_file(file_id)
            if file_info and file_info.item:
                mime_type = magic.from_buffer(file_info.item.read(2048), mime=True)
                CDEFile.objects.filter(pk=file_id).update(mime_type=mime_type)
        except Exception as e:
            logger.info(f"Cannot set mime_type for CDEFile with id={file_id}, filename={file_name}: {str(e)}")


class Migration(migrations.Migration):

    dependencies = [
        ('rdrf', '0127_cdefile_mime_type'),
    ]

    operations = [
        migrations.RunPython(
            set_mime_type, migrations.RunPython.noop
        )
    ]