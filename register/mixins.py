from collections import deque
import datetime
import itertools
from django import forms
from django_pandas.io import read_frame
from register.models import User,Shops,UserData
import pandas as pd
import numpy as np
from django.shortcuts import redirect, render, get_object_or_404
from django.shortcuts import render
from bs4 import BeautifulSoup
import urllib.request
import re

class NoMixin():
    """スケジュール付きの、月間カレンダーを提供するMixin"""

    def get_no(self):
        """それぞれの日と紐づくフォームを作成する"""
        lookup = {
            'shops__pk': self.kwargs.get('shop_pk'),
            
        }
        shop = self.kwargs['shop_pk']
        user= User.objects.filter(shops__shop=shop)
        b =[]
        for a in user:
            b.append(a)
        # queryset = UserData.objects.all()
        queryset = UserData.objects.filter(user__shops__shop=shop).order_by('no')
        print(queryset)
        count=(len(user))
        users=[]
        FormClass = forms.modelformset_factory(self.model, self.form_class, extra=count,max_num=count)
        if self.request.method == 'POST':
            formset = self.month_formset = FormClass(self.request.POST)
        else:
            formset = self.month_formset = FormClass(queryset=queryset)
            for bound_form in formset.initial_forms:
                    instance = bound_form.instance
                    user = instance.user
                    if user in b:
                        u={user:bound_form}
                        users.append(u)
                    else:
                        print(88888)
                        
        formset = {
            'users': users,
        }
        return formset
    def get_member_no(self):
        context = self.get_no()
        # context['user_forms'] = self.get_no()
        context['month_formset'] = self.month_formset
        
        return context
 