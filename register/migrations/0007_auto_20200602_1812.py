# Generated by Django 3.0.4 on 2020-06-02 09:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0006_auto_20200602_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shops',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_shop', to=settings.AUTH_USER_MODEL),
        ),
    ]