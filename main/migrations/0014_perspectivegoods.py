# Generated by Django 2.2.7 on 2020-07-13 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20200713_2027'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerspectiveGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, verbose_name='Название')),
                ('mark', models.CharField(blank=True, max_length=200, verbose_name='Маркировка')),
                ('D_field', models.CharField(blank=True, max_length=200, verbose_name='D, мм')),
                ('dp_field', models.CharField(blank=True, max_length=200, verbose_name='d постели, мм')),
                ('depth', models.CharField(blank=True, max_length=200, verbose_name='Толщина, мм')),
                ('width', models.CharField(blank=True, max_length=200, verbose_name='Ширина, мм')),
                ('using', models.CharField(blank=True, max_length=200, verbose_name='Применение')),
            ],
            options={
                'verbose_name': 'Перспективная продукция',
                'verbose_name_plural': 'Перспективная продукция',
            },
        ),
    ]