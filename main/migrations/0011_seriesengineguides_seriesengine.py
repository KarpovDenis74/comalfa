# Generated by Django 2.2.7 on 2020-07-08 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_seriesengine_seriesengineguides'),
    ]

    operations = [
        migrations.AddField(
            model_name='seriesengineguides',
            name='seriesEngine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.SeriesEngine', verbose_name='Серия двигателя'),
        ),
    ]