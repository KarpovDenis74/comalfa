# Generated by Django 2.2.7 on 2020-06-14 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='visible',
            field=models.BooleanField(default=True, verbose_name='Показывать новость'),
        ),
    ]
