# Generated by Django 2.2.7 on 2020-07-02 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20200618_0133'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='Gallery_images', verbose_name='Изображение')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
                ('description', models.CharField(max_length=200, verbose_name='Описание')),
            ],
        ),
        migrations.AlterField(
            model_name='engine',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='Engine_images', verbose_name='Схема'),
        ),
        migrations.AlterField(
            model_name='engine',
            name='manufactured',
            field=models.CharField(blank=True, max_length=200, verbose_name='Производитель'),
        ),
        migrations.AlterField(
            model_name='engineunits',
            name='img',
            field=models.ImageField(blank=True, upload_to='EngineUnits_images', verbose_name='Схема'),
        ),
        migrations.AlterField(
            model_name='parts',
            name='marks',
            field=models.CharField(blank=True, max_length=600, null=True, verbose_name='Маркировки'),
        ),
        migrations.AlterField(
            model_name='parts',
            name='notes',
            field=models.CharField(blank=True, max_length=600, null=True, verbose_name='Примечание'),
        ),
        migrations.AlterField(
            model_name='parts',
            name='position',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Позиция'),
        ),
        migrations.AlterField(
            model_name='parts',
            name='quantity',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='Кол-во на двигатель'),
        ),
    ]