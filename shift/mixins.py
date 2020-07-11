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


class BaseCalendarMixin:
    """カレンダー関連Mixinの、基底クラス"""
    first_weekday = 0  # 0は月曜から、1は火曜から。6なら日曜日からになります。お望みなら、継承したビューで指定してください。
    week_names = ['月', '火', '水', '木', '金', '土', '日']  # これは、月曜日から書くことを想定します。['Mon', 'Tue'...

    def setup_calendar(self):
        """内部カレンダーの設定処理
        calendar.Calendarクラスの機能を利用するため、インスタンス化します。
        Calendarクラスのmonthdatescalendarメソッドを利用していますが、デフォルトが月曜日からで、
        火曜日から表示したい(first_weekday=1)、といったケースに対応するためのセットアップ処理です。
        """
        self._calendar = calendar.Calendar(self.first_weekday)

    def get_week_names(self):
        """first_weekday(最初に表示される曜日)にあわせて、week_namesをシフトする"""
        week_names = deque(self.week_names)
        week_names.rotate(-self.first_weekday)  # リスト内の要素を右に1つずつ移動...なんてときは、dequeを使うと中々面白いです
        return week_names


class MonthCalendarMixin(BaseCalendarMixin):
    """月間カレンダーの機能を提供するMixin"""

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

            if date.month ==12 and date.day >10:
                month = 1
                year = date.year +1
                dtm = calendar.monthrange(year,month)[1]
                date = datetime.date(year = int(year),month=int(month),day = int(1))
                dtlist = [date + datetime.timedelta(days =day) for day in range(0,15)]
                return dtlist
            if date.month ==1  and  date.day ==1:
                month =12
                year = date.year-1
                dtm = calendar.monthrange(year,month)[1]
                date = datetime.date(year = int(year),month=int(month),day = int(15))
                dtlist = [date + datetime.timedelta(days =day) for day in range(1,dtm-14)]
                return dtlist

            if date.month != 12 and date.day < 21 and date.day > 4:
                dtm = calendar.monthrange(year,month)[1]
                date = datetime.date(year = int(year),month=int(month+1),day = int(1))
                dtlist = [date + datetime.timedelta(days =day) for day in range(0,15)]
                return dtlist
            if date.day < 6:
                dtm = calendar.monthrange(year,month)[1]
                date = datetime.date(year = int(year),month=int(month),day = int(15))
                dtlist = [date + datetime.timedelta(days =day) for day in range(1,dtm-14)]
                return dtlist
            if date.day > 20:
                month =month-1
                dtm = calendar.monthrange(year,month)[1]
                date = datetime.date(year = int(year),month=int(month),day = int(15))
                dtlist = [date + datetime.timedelta(days =day) for day in range(1,dtm-14)]
                return dtlist

        else:
            date = datetime.date.today()
            year =int(date.year)
            month=int(date.month)
            day=int(date.day)
            if date.day < 21 and date.day > 5:
                date = datetime.date(year = int(year),month=int(month+1),day = int(1))
                dtlist = [date + datetime.timedelta(days =day) for day in range(0,15)]
                return dtlist
            if date.day < 6:
                dtm = calendar.monthrange(year,month)[1]
                date = datetime.date(year = int(year),month=int(month),day = int(15))
                dtlist = [date + datetime.timedelta(days =day) for day in range(1,dtm-14)]
                return dtlist
            if date.day > 20:
                month = month + 1
                dtm = calendar.monthrange(year,month)[1]
                date = datetime.date(year = int(year),month=int(month),day = int(15))
                dtlist = [date + datetime.timedelta(days =day) for day in range(1,dtm-14)]
                return dtlist
            if date.month ==12 and date.day < 21 and date.day > 5:
                month = 1
                year = date.year +1
                dtm = calendar.monthrange(year,month)[1]
                date = datetime.date(year = int(year),month=int(month),day = int(1))
                dtlist = [date + datetime.timedelta(days =day) for day in range(0,15)]
                return dtlist


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



    def get_month_calendar(self):
        """月間カレンダー情報の入った辞書を返す"""
        self.setup_calendar()
        days = self.get_week_days()
        first = days[0]
        last = days[-1]
        ago = self.get_previous_week(first)
        calendar_data = {
            'now': datetime.date.today(),
            'month_days': days,

            'month_previous': ago,
            'month_next': first,
            'week_names': self.name(),
        }
        return calendar_data


class WeekCalendarMixin(BaseCalendarMixin):
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

            if date.month ==12 and date.day >10:
                month = 1
                year = date.year +1
                dtm = calendar.monthrange(year,month)[1]
                date = datetime.date(year = int(year),month=int(month),day = int(1))
                dtlist = [date + datetime.timedelta(days =day) for day in range(0,15)]
                return dtlist
            if date.month ==1  and  date.day ==1:
                month =12
                year = date.year-1
                dtm = calendar.monthrange(year,month)[1]
                date = datetime.date(year = int(year),month=int(month),day = int(15))
                dtlist = [date + datetime.timedelta(days =day) for day in range(1,dtm-14)]
                return dtlist

            if date.month != 12 and date.day < 21 and date.day > 4:
                dtm = calendar.monthrange(year,month)[1]
                date = datetime.date(year = int(year),month=int(month+1),day = int(1))
                dtlist = [date + datetime.timedelta(days =day) for day in range(0,15)]
                return dtlist
            if date.day < 6:
                dtm = calendar.monthrange(year,month)[1]
                date = datetime.date(year = int(year),month=int(month),day = int(15))
                dtlist = [date + datetime.timedelta(days =day) for day in range(1,dtm-14)]
                return dtlist
            if date.day > 20:
                month =month-1
                dtm = calendar.monthrange(year,month)[1]
                date = datetime.date(year = int(year),month=int(month),day = int(15))
                dtlist = [date + datetime.timedelta(days =day) for day in range(1,dtm-14)]
                return dtlist

        else:
            date = datetime.date.today()
            year =int(date.year)
            month=int(date.month)
            day=int(date.day)
            if date.day < 21 and date.day > 5:
                date = datetime.date(year = int(year),month=int(month+1),day = int(1))
                dtlist = [date + datetime.timedelta(days =day) for day in range(0,15)]
                return dtlist
            if date.day < 6:
                dtm = calendar.monthrange(year,month)[1]
                date = datetime.date(year = int(year),month=int(month),day = int(15))
                dtlist = [date + datetime.timedelta(days =day) for day in range(1,dtm-14)]
                return dtlist
            if date.day > 20:
                month = month + 1
                dtm = calendar.monthrange(year,month)[1]
                date = datetime.date(year = int(year),month=int(month),day = int(15))
                dtlist = [date + datetime.timedelta(days =day) for day in range(1,dtm-14)]
                return dtlist
            if date.month ==12 and date.day < 21 and date.day > 5:
                month = 1
                year = date.year +1
                dtm = calendar.monthrange(year,month)[1]
                date = datetime.date(year = int(year),month=int(month),day = int(1))
                dtlist = [date + datetime.timedelta(days =day) for day in range(0,15)]
                return dtlist


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


class ShiftWithScheduleMixin(WeekCalendarMixin):

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
                if time == '-':
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
                if time == '-':
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
                if time == '-':
                        time=None
                
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

class ShopShiftWithScheduleMixin(WeekCalendarMixin):

    def get_week_schedules(self, start, end, days):
        
        shop = self.kwargs['shops_pk']
        user= User.objects.filter(shops__shop=shop)
        q =Shop_config.objects.filter(shops__shop=shop)
    
        b =[]
        for a in user:
            b.append(a)
        lookup = {
            '{}__range'.format(self.date_field): (start, end),
                 
        }
        queryset = self.model.objects.filter(**lookup).order_by('user__userdata__start_day')
        days = {day: [] for day in days}   
        df = pd.DataFrame(days)
        # df.loc["希望人数"]=0
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
                    if time == '-':
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
                    if time == '-':
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
                    if time == '-':
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
                  
        # for shop_config_day,hope_pa in zip(queryset,df_num):
        #     # print(shop_config_day.day_need)
        #     if shop[0] == shop_config_day.shops:
        #         date = shop_config_day.date
        #         need = shop_config_day.day_need
        #         hope = hope_pa -need
        #         # print(hope_pa,need,"あ",hope,date)
        #         df.at["過不足",date] =hope
        #         df.fillna(" ", inplace=True)
        #     else:
        #         pass        
        return df

    def get_week_calendar(self):
        calendar_context = super().get_week_calendar()
        calendar_context['df'] = self.get_week_schedules(
            calendar_context['week_first'],
            calendar_context['week_last'],
            calendar_context['week_days']
        )
        return calendar_context 

class MasterMixin(MonthCalendarMixin):

    def get_month_forms(self, start, end, days):
        """それぞれの日と紐づくフォームを作成する"""
        lookup = {
            '{}__range'.format(self.date_field): (start, end),
            
        }
        shop = self.kwargs['shop_pk']
        user= User.objects.filter(shops__shop=shop)
    
        b =[]
        for a in user:
            b.append(a)
        queryset = self.model.objects.filter(**lookup,shops__shop=shop).order_by('user__userdata__start_day')
        set=[]
        count=(len(queryset))
        for per in queryset:
            if per.user in b:
                last=per.user.last_name
                first=per.user.first_name
                user=last+' '+first
                set.append(user)
        FormClass = forms.modelformset_factory(self.model, self.form_class, extra=count,max_num=count)
        if self.request.method == 'POST':

            formset = self.month_formset = FormClass(self.request.POST)
        else:
            formset = self.month_formset = FormClass(queryset=queryset)
            dates =[]
            days = {day: [] for day in days}   
            df = pd.DataFrame(days)
            a=1
            # ↓新しいフォームが作成されないようにデータのある日付を一回消してる
            # for bound_form in formset.initial_forms:
            #     instance = bound_form.instance
            #     date = getattr(instance, self.date_field)
            #     dates.append(date)
                
            #     days.remove(date)   
            users={user:[] for user in set }
            day_forms = {day: [] for day in days }
            # ↓初回作成用【2回目以降は多分通らない】
            # for empty_form, (date, empty_list) in zip(formset.extra_forms, day_forms.items()):
            #     empty_form.initial = {self.date_field: date}
            #     empty_list.append(empty_form)
            a=1
            for bound_form,user in zip(formset.initial_forms,set):
                if a==1:
                    instance = bound_form.instance
                    date = getattr(instance, self.date_field)
                    # d2 ={date:[vou]}
                    # d2[date].append(bound_form)   
                    ddf =pd.DataFrame({date:[bound_form]},index =[user])
                    df = pd.concat([df,ddf],axis=0)
                    df.fillna(" ", inplace=True)
                    b=user
                    a=2
                elif user != b: 
                    instance = bound_form.instance
                    date = getattr(instance, self.date_field)
                    ddf =pd.DataFrame({date:[bound_form]},index =[user])
                    df = pd.concat([df,ddf],axis=0)
                    df.fillna(" ", inplace=True)
                    b=user
                    print(df)
                else:
                    instance = bound_form.instance
                    date = getattr(instance, self.date_field)
                    df.at[user,date] =bound_form
                    df.fillna(" ", inplace=True)
            formset=df
            # for bound_form,user in zip(formset.initial_forms,set):
            #     if a==1:
            #         b=user
            #         instance = bound_form.instance
            #         date = getattr(instance, self.date_field)
            #         d2 ={date:[]}
            #         d2[date].append(bound_form)   
            #         day_forms.update(d2)
            #         aa={user:[]}
            #         aa[user].append(day_forms)
            #         users.update(aa)
            #         a=2
            #     if user != b:
            #         day_forms = {day: [] for day in days }
                
            #         u={user:[]}
            #         u=[user].append(user)
            #         b=user
            #         instance = bound_form.instance
            #         date = getattr(instance, self.date_field)
            #         d2 ={date:[]}
            #         d2[date].append(bound_form)   
            #         day_forms.update(d2)
            #         aa={user:[]}
            #         aa[user].append(day_forms)
            #         users.update(aa)
            #     else:
            #         instance = bound_form.instance
            #         date = getattr(instance, self.date_field)
            #         d2 ={date:[]}
            #         d2[date].append(bound_form)   
            #         day_forms.update(d2)
            #         aa={user:[]}
            #         aa[user].append(day_forms)
            #         users.update(aa)
            #         b=user
            # print(users)
            
            # day_forms = sorted(day_forms.items())
            # day_forms=dict(day_forms)
        return formset

    def get_month_calendar(self):
        calendar_context = super().get_month_calendar()
        month_days = calendar_context['month_days']
        month_first = month_days[0]
        month_last = month_days[-1]
        calendar_context['month_day_forms'] = self.get_month_forms(
            month_first,
            month_last,
            month_days
        )
        
        return calendar_context

class WeekWithScheduleMixin(WeekCalendarMixin):
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


class MonthWithScheduleMixin(MonthCalendarMixin):
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
        calendar_context = super().get_month_calendar()
        month_days = calendar_context['month_days']
        month_first = month_days[0][0]
        month_last = month_days[-1][-1]
        calendar_context['month_day_schedules'] = self.get_month_schedules(
            month_first,
            month_last,
            month_days
        )
        return calendar_context


class MonthWithFormsMixin(MonthCalendarMixin):
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
        # ↓新しいフォームが作成されないようにデータのある日付を一回消してる
        for bound_form in formset.initial_forms:
            instance = bound_form.instance
            date = getattr(instance, self.date_field)
            dates.append(date)
            days.remove(date)
        day_forms = {day: [] for day in days }
        # ↓初回作成用【2回目以降は多分通らない】
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
        calendar_context = super().get_month_calendar()
        month_days = calendar_context['month_days']
        month_first = month_days[0]
        month_last = month_days[-1]
        calendar_context['month_day_forms'] = self.get_month_forms(
            month_first,
            month_last,
            month_days
        )
        calendar_context['month_formset'] = self.month_formset
        
        return calendar_context

class Day_configMixin(MonthCalendarMixin):
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
        calendar_context = super().get_month_calendar()
        month_days = calendar_context['month_days']
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

            if date.day < 21 and date.day > 5:
                dtm = calendar.monthrange(year,month)[1]
                date = datetime.date(year = int(year),month=int(month),day=int(15))
                dtlist = [date + datetime.timedelta(days =day) for day in range(1,dtm-14)]
                return dtlist
            if date.day < 6:
                date = datetime.date(year = int(year),month=int(month),day = int(1))
                dtlist = [date + datetime.timedelta(days =day) for day in range(0,15)]
                return dtlist

        else:
            pass
        #     date = datetime.date.today()
        #     year =int(date.year)
        #     month=int(date.month)
        #     day=int(date.day)
        #     if date.day < 21 and date.day > 5:
        #         dtm = calendar.monthrange(year,month)[1]
        #         date = datetime.date(year = int(year),month=int(month),day = int(15))
        #         dtlist = [date + datetime.timedelta(days =day) for day in range(1,dtm-14)]

        #         return dtlist
        #     if date.day < 6:
        #         date = datetime.date(year = int(year),month=int(month+1),day = int(1))
        #         dtlist = [date + datetime.timedelta(days =day) for day in range(0,15)]
        #         return dtlist
            


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