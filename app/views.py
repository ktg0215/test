import datetime
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from .forms import BS4ScheduleForm, SimpleScheduleForm
from .models import Schedule
from . import mixins
from .models import User
from django_pandas.io import read_frame
from register.models import Shops

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
                print(schedule.shops)
                schedule.save()
                shops.save()
                user.save()
            return redirect('app:week_with_schedule', user_pk=user_pk)

        return render(request, self.template_name, context)
