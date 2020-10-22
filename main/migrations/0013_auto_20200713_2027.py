# Generated by Django 2.2.7 on 2020-07-13 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_engine_seriesengine'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, verbose_name='Название')),
                ('count', models.CharField(blank=True, max_length=200, verbose_name='Ед.')),
                ('price', models.CharField(blank=True, max_length=200, verbose_name='Цена без НДС')),
                ('discount', models.CharField(blank=True, max_length=200, verbose_name='Скидка')),
                ('cost', models.CharField(blank=True, max_length=200, verbose_name='Цена со скидкой')),
            ],
            options={
                'verbose_name': 'Товары со скидкой',
                'verbose_name_plural': 'Товары со скидкой',
            },
        ),
        migrations.RemoveField(
            model_name='engine',
            name='manufactured',
        ),
    ]
