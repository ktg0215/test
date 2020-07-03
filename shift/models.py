from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from django.utils import timezone
from django.conf import settings
from register.models import Shops

SUB_START = (
    
    ('1', '14'),
    ('2', '16'),
    ('3', '17'),
    ('4', '17.5'),
    ('5', '18'),
    ('6', '18.5'),
    ('7', '19'),
    ('8', '19.5'),
    ('9', '20'),
    ('10', '〇'),
)
SUB_END = (
    
    ('1', '22'),
    ('2', '23'),
    ('3', '〇'),

)

class Schedule(models.Model):
    """スケジュール"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー', on_delete=models.SET_NULL, blank=True, null=True,related_name = "user_schedule")
    start_time = models.CharField('開始時間', choices= SUB_START, max_length=50,blank=True,default="0")
    end_time = models.CharField('終了時間', choices= SUB_END, max_length=50,blank=True,default="0")
    date = models.DateField('日付')
    shops = models.ForeignKey(Shops, verbose_name='店舗', on_delete=models.CASCADE,blank=True)


    def __str__(self):
        return f"{self.user.last_name} {self.date}"

class Shop_config(models.Model):
    shops = models.OneToOneField(Shops,on_delete=models.CASCADE)
    base_pa_a = models.IntegerField('平日',default=0)
    base_pa_b = models.IntegerField('祝前',default=0)
    base_pa_c = models.IntegerField('土日',default=0)

class Shop_config_day(models.Model):
    shops = models.ForeignKey(Shops, verbose_name='店舗', on_delete=models.CASCADE,blank=True)
    day_need = models.IntegerField('必要人数',default=0)
    date = models.DateField('日付')

    def __str__(self):
        return f"{self.shops.get_shop_display()} {self.date}"



