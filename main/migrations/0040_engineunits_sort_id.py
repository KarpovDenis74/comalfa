# Generated by Django 2.2.7 on 2020-08-30 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_maingoods_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='engineunits',
            name='sort_id',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Порядковый номер'),
        ),
    ]