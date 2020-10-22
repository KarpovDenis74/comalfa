# Generated by Django 2.2.7 on 2020-08-23 23:58

import django.core.files.storage
from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_auto_20200823_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engine',
            name='filePDF',
            field=models.FileField(blank=True, default='default_pdf.pdf', null=True, storage=django.core.files.storage.FileSystemStorage(location='/home/sammy/comalfa/media'), upload_to=main.models.Engine.get_filePDF_path, verbose_name='Документ pdf'),
        ),
    ]