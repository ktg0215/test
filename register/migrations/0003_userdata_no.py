# Generated by Django 3.0.8 on 2020-07-18 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_auto_20200716_0116'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='no',
            field=models.CharField(blank=True, max_length=3),
        ),
    ]