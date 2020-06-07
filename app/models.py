from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from django.utils import timezone
from django.conf import settings
from django_pandas.managers import DataFrameManager
from register.models import Shops

SUB_START = (
    ('0', '✕'),
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
    ('0', '✕'),
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

    objects = DataFrameManager()

    def __int__(self):
        return self.date

"""

submissiontime = (
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


class Profile(models.Model):
    phone = models.CharField("生年月日", max_length=255, blank=True)
    gender = models.CharField("所属店舗", choices=submissiontime, blank=True,)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
"""
