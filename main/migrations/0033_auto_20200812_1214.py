# Generated by Django 2.2.7 on 2020-08-12 12:14

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_auto_20200730_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engine',
            name='filePDF',
            field=models.FileField(blank=True, default='settings.MEDIA_ROOT/images/6png.png', null=True, upload_to=main.models.Engine.get_filePDF_path, verbose_name='Документ pdf'),
        ),
    ]