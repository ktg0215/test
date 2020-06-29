import datetime
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from .forms import BS4ScheduleForm, SimpleScheduleForm, Shop_base_configForm, Shop_config_dayForm
from .models import Schedule,Shop_config,Shop_config_day
from . import mixins
from .models import User
from register.models import Shops
from django.urls import reverse

User = get_user_model()


class ShiftList(mixins.ShiftWithScheduleMixin, generic.ListView):
    """ユーザーの一覧"""
    model = Schedule
    template_name = 'app/shift_list.html'
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context
        
class ShopShiftList(mixins.ShopShiftWithScheduleMixin, generic.TemplateView):
    """ユーザーの一覧"""
    model = Schedule
    template_name = 'app/shopshift_list.html'
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = get_object_or_404(Shops, pk=self.kwargs['shops_pk'])
        context['shops']= User.objects.filter(shops__shop=shop)
        context['shopnum']=self.kwargs['shops_pk']
        context['config']= Shop_config_day.objects.filter(shops=shop)
        context['base_config']= Shop_config.objects.filter(shops=shop)
        base_config= Shop_config.objects.filter(shops=shop)

        print(base_config)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context       

class WeekWithScheduleCalendar(mixins.WeekWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの週間カレンダーを表示するビュー"""
    template_name = 'app/week_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, pk=self.kwargs['user_pk'])
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context


class MonthWithScheduleCalendar(mixins.MonthWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの月間カレンダーを表示するビュー"""
    template_name = 'app/month_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, pk=self.kwargs['user_pk'])
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class MyCalendar(mixins.MonthCalendarMixin, mixins.WeekWithScheduleMixin, generic.CreateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""
    template_name = 'app/mycalendar.html'
    model = Schedule
    date_field = 'date'
    form_class = BS4ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, pk=self.kwargs['user_pk'])
        
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(week_calendar_context)
        context.update(month_calendar_context)
        return context

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        user_pk = self.kwargs['user_pk']
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        schedule = form.save(commit=False)
        schedule.date = date
        schedule.user = get_object_or_404(User, pk=user_pk)
        schedule.save()
        return redirect('app:mycalendar', year=date.year, month=date.month, day=date.day, user_pk=user_pk)


class MonthWithFormsCalendar(mixins.MonthWithFormsMixin, generic.View):
    """フォーム付きの月間カレンダーを表示するビュー"""
    template_name = 'app/month_with_forms.html'
    model = Schedule
    date_field = 'date'
    form_class = SimpleScheduleForm

    def get(self, request, **kwargs):

        context = self.get_month_calendar()
        context['user'] = get_object_or_404(User, pk=self.kwargs['user_pk'])

        return render(request, self.template_name, context)
    

    def post(self, request, **kwargs):

        context = self.get_month_calendar()
        user_pk = self.kwargs['user_pk']
        user = get_object_or_404(User, pk=user_pk)
        context['user'] = user
        shops = user.shops
        formset = context['month_formset']
        if formset.is_valid():

            instances = formset.save(commit=False)
            for schedule in instances:
                schedule.user = user
                user.schedule = schedule
                shops.schedule = schedule
                schedule.shops = user.shops
                schedule.save()
                shops.save()
                user.save()
            return redirect('app:week_with_schedule', user_pk=user_pk)

        return render(request, self.template_name, context)

class Shop_base_views(generic.CreateView):
    model = Shop_config
    template_name= 'app/shop_config.html'
    form_class = Shop_base_configForm
    success_url = "shift/shift_list"
    def get_initial(self):
        initial = super().get_initial()
        initial["shops"] = self.request.user.shops
        return initial


 
class Shop_baseupdate_views(generic.UpdateView):
    model = Shop_config
    template_name= 'app/shop_config.html'
    form_class = Shop_base_configForm
    
    success_url = '/'
 
class Shop_config_day_views(mixins.Day_configMixin, generic.View):
    model = Shop_config_day
    template_name = 'app/day_config.html'
    date_field = 'date'
    form_class= Shop_config_dayForm

    def get(self, request, **kwargs):

        context = self.get_month_calendar()
        context['shop'] = get_object_or_404(User, pk=self.kwargs['shop_pk'])

        return render(request, self.template_name, context)
    

    def post(self, request, **kwargs):

        context = self.get_month_calendar()
        shop_pk = self.kwargs['shop_pk']
        shops = get_object_or_404(Shops, pk=shop_pk)
        shops=User.objects.filter(shops__shop=shops)
        context['shops'] = shops
        formset = context['month_formset']
        if formset.is_valid():
            instances = formset.save(commit=False)
            for shop_config_day in instances:
                shops.shop_config_day = shop_config_day
                shop_config_day.shops = shops
                shop_config_day.save()
                shops.save()
            return redirect('app:shift_list')

        return render(request, self.template_name, context)



