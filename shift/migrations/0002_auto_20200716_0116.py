# Generated by Django 3.0.8 on 2020-07-15 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shift', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='end_at',
            field=models.CharField(blank=True, choices=[('1', '22'), ('2', '23'), ('3', '〇')], max_length=50),
        ),
        migrations.AddField(
            model_name='schedule',
            name='start_at',
            field=models.CharField(blank=True, choices=[('1', '14'), ('2', '16'), ('3', '17'), ('4', '17.5'), ('5', '18'), ('6', '18.5'), ('7', '19'), ('8', '19.5'), ('9', '20'), ('10', '〇')], max_length=50),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='end_time',
            field=models.CharField(blank=True, choices=[('1', '22'), ('2', '23'), ('3', '〇')], default=0, max_length=50, verbose_name='終了時間'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start_time',
            field=models.CharField(blank=True, choices=[('1', '14'), ('2', '16'), ('3', '17'), ('4', '17.5'), ('5', '18'), ('6', '18.5'), ('7', '19'), ('8', '19.5'), ('9', '20'), ('10', '〇')], default=0, max_length=50, verbose_name='開始時間'),
        ),
    ]