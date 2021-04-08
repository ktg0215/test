# Generated by Django 3.0.7 on 2020-06-24 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shopdata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.DateField(blank=True, verbose_name='日付')),
                ('shop', models.CharField(blank=True, choices=[('0', '目黒'), ('1', '上野広小路'), ('2', '神保町白山通り'), ('3', '北千住')], max_length=10, verbose_name='店舗')),
                ('sales', models.IntegerField(blank=True, default='0', verbose_name='売上')),
                ('gest', models.IntegerField(blank=True, default='0', verbose_name='客数')),
                ('gloup', models.IntegerField(blank=True, default='0', verbose_name='組数')),
                ('one', models.IntegerField(blank=True, default='0', verbose_name='単価')),
                ('maketime', models.IntegerField(blank=True, default='0', verbose_name='生産性')),
                ('labor', models.FloatField(blank=True, default='0', verbose_name='人件費率')),
            ],
            options={
                'verbose_name': '計数管理',
                'verbose_name_plural': '一覧',
            },
        ),
    ]