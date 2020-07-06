# Generated by Django 3.0.8 on 2020-07-06 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('register', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop_config_day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_need', models.IntegerField(default=0, verbose_name='必要人数')),
                ('date', models.DateField(verbose_name='日付')),
                ('shops', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='register.Shops', verbose_name='店舗')),
            ],
        ),
        migrations.CreateModel(
            name='Shop_config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_pa_a', models.IntegerField(default=0, verbose_name='平日')),
                ('base_pa_b', models.IntegerField(default=0, verbose_name='祝前')),
                ('base_pa_c', models.IntegerField(default=0, verbose_name='土日')),
                ('shops', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='register.Shops')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.CharField(blank=True, choices=[('1', '14'), ('2', '16'), ('3', '17'), ('4', '17.5'), ('5', '18'), ('6', '18.5'), ('7', '19'), ('8', '19.5'), ('9', '20'), ('10', '〇')], default='0', max_length=50, verbose_name='開始時間')),
                ('end_time', models.CharField(blank=True, choices=[('1', '22'), ('2', '23'), ('3', '〇')], default='0', max_length=50, verbose_name='終了時間')),
                ('date', models.DateField(verbose_name='日付')),
                ('shops', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='register.Shops', verbose_name='店舗')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_schedule', to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
    ]
