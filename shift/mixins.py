import calendar
from collections import deque
import datetime
import itertools
from django import forms
from django_pandas.io import read_frame
from register.models import User,Shops
import pandas as pd
import numpy as np
from .models import Schedule,Shop_config_day,Shop_config
from django.shortcuts import redirect, render, get_object_or_404
from django.shortcuts import render
from bs4 import BeautifulSoup
import urllib.request
import re


class BaseCalendarMixin:
    """カレンダー関連Mixinの、基底クラス"""
    first_weekday = 4  # 0は月曜から、1は火曜から。6なら日曜日からになります。お望みなら、継承したビューで指定してください。
    week_names = ['月', '火', '水', '木', '金', '土', '日']  # これは、月曜日から書くことを想定します。['Mon', 'Tue'...

    def setup_calendar(self):
        self._calendar = calendar.Calendar(self.first_weekday)

    def get_week_names(self):
        """first_weekday(最初に表示される曜日)にあわせて、week_namesをシフトする"""
        week_names = deque(self.week_names)
        week_names.rotate(-self.first_weekday)  # リスト内の要素を右に1つずつ移動...なんてときは、dequeを使うと中々面白いです
        return week_names

class PizzaMixin(BaseCalendarMixin):
    """週間カレンダーの機能を提供するMixin"""

    def get_week_days(self):
        """その週の日を全て返す"""
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        for week in self._calendar.monthdatescalendar(date.year, date.month):
            if date in week:  # 週ごとに取り出され、中身は全てdatetime.date型。該当の日が含まれていれば、それが今回表示すべき週です
                return week

    def get_week_calendar(self):
        """週間カレンダー情報の入った辞書を返す"""
        self.setup_calendar()
        days = self.get_week_days()
        first = days[0]
        last = days[-1]
        calendar_data = {
            'now': datetime.date.today(),
            'week_days': days,
            'week_previous': first - datetime.timedelta(days=7),
            'week_next': first + datetime.timedelta(days=7),
            'week_names': self.get_week_names(),
            'week_first': first,
            'week_last': last,
        }
        return calendar_data
class ShiftWithScheduleMixin(PizzaMixin):

    def get_week_schedules(self, start, end, days):
        
        lookup = {
            '{}__range'.format(self.date_field): (start, end),
           
        }
        queryset = self.model.objects.filter(**lookup).order_by('user__userdata__start_day')
        days = {day: [] for day in days}   
        df = pd.DataFrame(days)
        df.loc["希望人数"]=0
     
        
        a=1
        for schedule in queryset:
            if a == 1:
                user=schedule.user.last_name+' '+schedule.user.first_name
                date= schedule.date
                start_time=schedule.get_start_time_display()
                end_time = schedule.get_end_time_display()
                time = start_time+'-'+end_time
                ddf =pd.DataFrame({date:time},index =[user])
                df = pd.concat([df,ddf],axis=0)
                df.fillna(" ", inplace=True)
                a = 2
                
            elif user != schedule.user.last_name+' '+schedule.user.first_name: 
                user=schedule.user.last_name+' '+schedule.user.first_name
                date= schedule.date

                start_time=schedule.get_start_time_display()
                end_time = schedule.get_end_time_display()
                time = start_time+'-'+end_time
                ddf =pd.DataFrame({date:time},index =[user])
                df = pd.concat([df,ddf],axis=0)
                df.fillna(" ", inplace=True)
                
            else:    
                user=schedule.user.last_name+' '+schedule.user.first_name
                date= schedule.date

                start_time=schedule.get_start_time_display()
                end_time = schedule.get_end_time_display()
                time = start_time+'-'+end_time
                
                # ddf =pd.DataFrame({date:time},index =[user])
                df[date]= df[date].astype(str)
                df.at[user,date] =time
                df.fillna(" ", inplace=True) 
               
        df.fillna(" ", inplace=True)
        # 提出人数確認↓ーーーーーーーーーー
        df_bool = (df == ' ')
        df_bool.sum()
        dfnum=[]
        for m in df_bool.sum():
            dfnum.append(m)
        num=len(df)-1 #全体人数
        df_num=[]
        for a in dfnum:
            b=num-a
            df_num.append(b)

        df.loc["希望人数"]=df_num
         

        return df

    def get_week_calendar(self):
        calendar_context = super().get_week_calendar()
        calendar_context['df'] = self.get_week_schedules(
            calendar_context['week_first'],
            calendar_context['week_last'],
            calendar_context['week_days']
        )
        return calendar_context

class ShopShiftWithScheduleMixin(PizzaMixin):

    def get_week_schedules(self, start, end, days):
        
        shop = self.kwargs['shops_pk']
        bet=shop
        user= User.objects.filter(shops__shop=shop)
        q =Shop_config.objects.filter(shops__shop=shop)
        print(shop)
    
        b =[]
        for a in user:
            b.append(a)
        lookup = {
            '{}__range'.format(self.date_field): (start, end),
                 
        }
        queryset = self.model.objects.filter(**lookup).order_by('user__userdata__start_day')
        days = {day: [] for day in days}   
        df = pd.DataFrame(days)
        df.loc["天気"]=None
        df.loc["降水確率"]=None
        df.loc["必要人数"]=0
        df.loc["過不足"]=0
        


        a=1
        for schedule in queryset:
            if schedule.user in b:
                if a == 1:
                    user=schedule.user.last_name+' '+schedule.user.first_name
                    date= schedule.date
                    start_time=schedule.get_start_time_display()
                    end_time = schedule.get_end_time_display()
                    time = start_time+'-'+end_time
                    if time =='-':
                        time=None
                    ddf =pd.DataFrame({date:time},index =[user])
                    df = pd.concat([df,ddf],axis=0)
                    df.fillna(" ", inplace=True)
                    a = 2
                    
                elif user != schedule.user.last_name+' '+schedule.user.first_name: 
                    user=schedule.user.last_name+' '+schedule.user.first_name
                    date= schedule.date

                    start_time=schedule.get_start_time_display()
                    end_time = schedule.get_end_time_display()
                    time = start_time+'-'+end_time
                    if time =='-':
                        time=None
                    ddf =pd.DataFrame({date:time},index =[user])
                    df = pd.concat([df,ddf],axis=0)
                    df.fillna(" ", inplace=True)
                    
                else:    
                    user=schedule.user.last_name+' '+schedule.user.first_name
                    date= schedule.date

                    start_time=schedule.get_start_time_display()
                    end_time = schedule.get_end_time_display()
                    time = start_time+'-'+end_time
                    if time =='-':
                        time=None
                    
                    # ddf =pd.DataFrame({date:time},index =[user])
                    df[date]= df[date].astype(str)
                    df.at[user,date] =time
                    df.fillna(" ", inplace=True)
            else:
                pass
                   
               
        df.fillna(" ", inplace=True)
        # 提出人数確認↓ーーーーーーーーーー
        df_bool = (df == ' ')
        df_bool.sum()
        dfnum=[]
        for m in df_bool.sum():
            dfnum.append(m)
        num=len(df)-2 #全体
        df_num=[]
        for a in dfnum:
            b=num-a
            df_num.append(b)

        # df.loc["希望人数"]=df_num
        # 必要人数---------------↓
        shop=Shops.objects.filter(shop=shop)

        lookup = {
            '{}__range'.format(self.date_field): (start, end),
        }
        queryset = Shop_config_day.objects.filter(**lookup)
        for shop_config_day in queryset:
            if shop[0] == shop_config_day.shops:
                date = shop_config_day.date
                need = shop_config_day.day_need
                df.at["必要人数",date] =int(need)
                df.fillna(" ", inplace=True)
            else:
                pass
        s=df.loc["必要人数"]  
        p=[]   
        for need in s:
            p.append(need)
        o=[]
        for s,hope_pa in zip(p,df_num):
            if isinstance(s, int):
                f=hope_pa-s
                o.append(f)  
            else:       
                s=0
                f=hope_pa-s
                o.append(f)
        df.loc["過不足"]=o 

        # 天気ーーーーーーーーーーー
        if bet==1:
            # 八潮↓
            url="https://tenki.jp/forecast/3/14/4310/11234/"
        elif bet==4:
            # 竹の塚↓
            url="https://tenki.jp/forecast/3/16/4410/13121/"
        elif bet==3:
            # 三郷↓
            url="https://tenki.jp/forecast/3/14/4310/11237/"
        elif bet==2:
            # 東川口↓
            url="https://tenki.jp/forecast/3/14/4310/11203/"
        elif bet==5:
            # 山室↓
            url="https://tenki.jp/forecast/4/19/5510/16201/"
        elif bet==6:
            # 奥田↓
            url="https://tenki.jp/forecast/4/19/5510/16201/"


        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html)
        cc=[]
        # ↑日
        dates=[tag.text for tag in soup(class_='date-box')]
        for a in dates:
            atime=datetime.datetime.strptime(a,'%m月%d日')
            date = datetime.date(2020,atime.month,atime.day)
            cc.append(date)
        tds=[tag for tag in soup('td',class_='weather-icon')]
        imgs=[]
        #↑画像
        for b in soup.find_all('td',class_='weather-icon'):
            for a in b.find_all('img',src=re.compile('^https://static.tenki.jp/images/icon/forecast-days-weather/')):
                imgs.append(a.get("src"))
        ames=[]        
        for ame in soup.find_all(class_='precip'):
            ames.append(ame.text)
            
        for (d,tenki,ame) in zip(cc,imgs,ames):
            if d in days:

                df.at['天気',d] =str(tenki)
                df.at['降水確率',d] =str(ame)
                df.fillna(" ", inplace=True)
            
             
        return df

    def get_week_calendar(self):
        calendar_context = super().get_week_calendar()
        calendar_context['df'] = self.get_week_schedules(
            calendar_context['week_first'],
            calendar_context['week_last'],
            calendar_context['week_days']
        )
        return calendar_context

class WeekWithScheduleMixin(PizzaMixin):
    """スケジュール付きの、週間カレンダーを提供するMixin"""

    def get_week_schedules(self, start, end, days):
        """それぞれの日とスケジュールを返す"""
        lookup = {
            # '例えば、date__range: (1日, 31日)'を動的に作る
            '{}__range'.format(self.date_field): (start, end),
            'user__pk': self.kwargs.get('user_pk'),
        }
        # 例えば、Schedule.objects.filter(date__range=(1日, 31日)) になる
        queryset = self.model.objects.filter(**lookup)

        # {1日のdatetime: 1日のスケジュール全て, 2日のdatetime: 2日の全て...}のような辞書を作る
        day_schedules = {day: [] for day in days}
        for schedule in queryset:
            schedule_date = getattr(schedule, self.date_field)
            day_schedules[schedule_date].append(schedule)
        return day_schedules

    def get_week_calendar(self):
        calendar_context = super().get_week_calendar()
        calendar_context['week_day_schedules'] = self.get_week_schedules(
            calendar_context['week_first'],
            calendar_context['week_last'],
            calendar_context['week_days']
        )
        return calendar_context


class MonthWithScheduleMixin(PizzaMixin):
    """スケジュール付きの、月間カレンダーを提供するMixin"""

    def get_month_schedules(self, start, end, days):
        """それぞれの日とスケジュールを返す"""
        lookup = {
            '{}__range'.format(self.date_field): (start, end),
            'user__pk': self.kwargs.get('user_pk'),
        }
        queryset = self.model.objects.filter(**lookup)

        day_schedules = {day: [] for week in days for day in week}
        for schedule in queryset:
            schedule_date = getattr(schedule, self.date_field)
            day_schedules[schedule_date].append(schedule)

        size = len(day_schedules)
        return [{key: day_schedules[key] for key in itertools.islice(day_schedules, i, i+7)} for i in range(0, size, 7)]

    def get_month_calendar(self):
        calendar_context = super().get_week_calendar()
        month_days = calendar_context['month_days']
        month_first = month_days[0][0]
        month_last = month_days[-1][-1]
        calendar_context['month_day_schedules'] = self.get_month_schedules(
            month_first,
            month_last,
            month_days
        )
        return calendar_context


class MonthWithFormsMixin(PizzaMixin):
    """スケジュール付きの、月間カレンダーを提供するMixin"""

    def get_month_forms(self, start, end, days):
        """それぞれの日と紐づくフォームを作成する"""
        lookup = {
            '{}__range'.format(self.date_field): (start, end),
            'user__pk': self.kwargs.get('user_pk'),
            
        }
        queryset = self.model.objects.filter(**lookup)
        days_count = len(days)
        FormClass = forms.modelformset_factory(self.model, self.form_class, extra=days_count,max_num=days_count)
        if self.request.method == 'POST':

            formset = self.month_formset = FormClass(self.request.POST)
        else:
            formset = self.month_formset = FormClass(queryset=queryset)
        dates =[]
        for bound_form in formset.initial_forms:
            
            instance = bound_form.instance
            date = getattr(instance, self.date_field)
            dates.append(date)
            days.remove(date)
        day_forms = {day: [] for day in days }

        for empty_form, (date, empty_list) in zip(formset.extra_forms, day_forms.items()):
            empty_form.initial = {self.date_field: date}
            empty_list.append(empty_form)

        for bound_form in formset.initial_forms:
            instance = bound_form.instance
            date = getattr(instance, self.date_field)
            d2 ={date:[]}
            d2[date].append(bound_form)   
            day_forms.update(d2)
        
        day_forms = sorted(day_forms.items())
        day_forms=dict(day_forms)


        return [{key: day_forms[key] for key in itertools.islice(day_forms, 0, days_count)}]

    def get_month_calendar(self):
        calendar_context = super().get_week_calendar()
        month_days = calendar_context['week_days']
        month_first = month_days[0]
        month_last = month_days[-1]
        calendar_context['month_day_forms'] = self.get_month_forms(
            month_first,
            month_last,
            month_days
        )
        calendar_context['month_formset'] = self.month_formset
        
        return calendar_context

class Day_configMixin(PizzaMixin):
    """スケジュール付きの、月間カレンダーを提供するMixin"""

    def get_month_forms(self, start, end, days):

        lookup = {
            '{}__range'.format(self.date_field): (start, end),
            'shops__pk': self.kwargs.get('shop_pk'),
            
        }
        queryset = self.model.objects.filter(**lookup)
        days_count = len(days)
        FormClass = forms.modelformset_factory(self.model, self.form_class, extra=days_count,max_num=days_count)
        if self.request.method == 'POST':

            formset = self.month_formset = FormClass(self.request.POST)
        else:
            formset = self.month_formset = FormClass(queryset=queryset)
        dates =[]
        for bound_form in formset.initial_forms:
            
            instance = bound_form.instance
            date = getattr(instance, self.date_field)
            
            dates.append(date)
            days.remove(date)
        day_forms = {day: [] for day in days }


        for empty_form, (date, empty_list) in zip(formset.extra_forms, day_forms.items()):
            empty_form.initial = {self.date_field: date}
            empty_list.append(empty_form)

        for bound_form in formset.initial_forms:
            instance = bound_form.instance
            date = getattr(instance, self.date_field)
            d2 ={date:[]}
            d2[date].append(bound_form)   
            day_forms.update(d2)
        
        day_forms = sorted(day_forms.items())
        day_forms=dict(day_forms)

        return [{key: day_forms[key] for key in itertools.islice(day_forms, 0, days_count)}]

    def get_month_calendar(self):
        calendar_context = super().get_week_calendar()
        month_days = calendar_context['week_days']
        month_first = month_days[0]
        month_last = month_days[-1]
        calendar_context['month_day_forms'] = self.get_month_forms(
            month_first,
            month_last,
            month_days
        )
        calendar_context['month_formset'] = self.month_formset
        
        return calendar_context
class Week_CsvMixin(BaseCalendarMixin):
    """週間カレンダーの機能を提供するMixin"""

    def get_previous_week(self, date):
        """前月を返す"""
        if date.month == 1 and date.day ==16:
            return date.replace(year=date.year-1, month=12,day=16)
        if date.month == 1 and date.day ==1:
            return date.replace(year=date.year-1, month=12,day=1)

        if date.day == 16:
            return date.replace(month =date.month -1 ,day = 16)
        if date.day == 1:
            return date.replace(month =date.month -1 ,day = 1)

    def get_week_days(self):
        """その週の日を全て返す"""
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        for week in self._calendar.monthdatescalendar(date.year, date.month):
            if date in week:  # 週ごとに取り出され、中身は全てdatetime.date型。該当の日が含まれていれば、それが今回表示すべき週です
                return week


    def name(self):
        weekname=['月','火','水','木','金','土','日']
        name=[]
        week=[]
        day = self.get_week_days()
        for l in day:
            name.append(l.weekday())
        for nn in name:
            week.append(weekname[nn])
        return week


    def get_week_calendar(self):
        """週間カレンダー情報の入った辞書を返す"""
        self.setup_calendar()
        days = self.get_week_days()
        first = days[0]
        last = days[-1]
        ago = self.get_previous_week(first)
        calendar_data = {
            'now': datetime.date.today(),
            'week_days': days,
            'week_previous': ago,
            'week_next': first ,
            'week_names': self.name(),
            'week_first': first,
            'week_last': last,
        }
        return calendar_data        

class CsvMixin(Week_CsvMixin):

    def get_week_schedules(self, start, end, days):
        
        # shop = get_object_or_404(Shops, pk=self.kwargs['shops_pk'])
        shop=self.kwargs['shops_pk']
        user= User.objects.filter(shops__shop=shop)
        
        b =[]
        for a in user:
            b.append(a)
        lookup = {
            '{}__range'.format(self.date_field): (start, end),
                 
        }
        queryset = self.model.objects.filter(**lookup)

        # -----日付のみ出力
        dd =[]
        for dday in days:
            d =dday.day
            dd.append(d)
        # ^^^^^    
        days = {day: [] for day in dd }   
        df = pd.DataFrame(days)
        
        a=1
        for schedule in queryset:
            
            if schedule.user in b:
                if a == 1:
                    user=schedule.user.last_name+' '+schedule.user.first_name
                    date= schedule.date
                    date=date.day
                    start_time=schedule.get_start_time_display()
                    end_time = schedule.get_end_time_display()
                    time = start_time+'-'+end_time
                    ddf =pd.DataFrame({date:time},index =[user])
                    df = pd.concat([df,ddf],axis=0)
                    df.fillna(" ", inplace=True)
                    a = 2
                    
                if user != schedule.user.last_name+' '+schedule.user.first_name: 
                    user=schedule.user.last_name+' '+schedule.user.first_name
                    date= schedule.date
                    date=date.day
                    start_time=schedule.get_start_time_display()
                    end_time = schedule.get_end_time_display()
                    time = start_time+'-'+end_time
                    ddf =pd.DataFrame({date:time},index =[user])
                    df = pd.concat([df,ddf],axis=0)
                    df.fillna(" ", inplace=True)
                    
                else:    
                    user=schedule.user.last_name+' '+schedule.user.first_name
                    date= schedule.date
                    date=date.day
                    start_time=schedule.get_start_time_display()
                    end_time = schedule.get_end_time_display()
                    time = start_time+'-'+end_time
                    ddf =pd.DataFrame({date:time},index =[user])
                    df[date]= df[date].astype(str)
                    df.at[user,date] =time
                    df.fillna(" ", inplace=True) 
        # csv保存-------------------        
        df.fillna(" ", inplace=True)

        return df
      

    def get_week_calendar(self):
        calendar_context = super().get_week_calendar()
        calendar_context['df'] = self.get_week_schedules(
            calendar_context['week_first'],
            calendar_context['week_last'],
            calendar_context['week_days']
        )

        return calendar_context

        