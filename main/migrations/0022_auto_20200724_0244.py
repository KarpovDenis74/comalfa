# Generated by Django 2.2.7 on 2020-07-24 02:44

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20200724_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engine',
            name='filePDF',
            field=models.FileField(upload_to=main.models.Engine.get_filePDF_path, verbose_name='Документ pdf'),
        ),
    ]
