from django.urls import path
from . import views

app_name = 'shift'

urlpatterns = [
    path('shift_list/', views.ShiftList.as_view(), name='shift_list'),
    path('shift_list/<int:year>/<int:month>/<int:day>/', views.ShiftList.as_view(), name='shift_list'),
    path('shop/<int:shops_pk>/shopshift_list/', views.ShopShiftList.as_view(), name='shopshift_list'),
    path('shop/<int:shops_pk>/shopshift_list/<int:year>/<int:month>/<int:day>/', views.ShopShiftList.as_view(), name='shopshift_list'),
    
    path('user/<int:user_pk>/week_with_schedule/', views.WeekWithScheduleCalendar.as_view(), name='week_with_schedule'),
    path(
        'user/<int:user_pk>/week_with_schedule/<int:year>/<int:month>/<int:day>/',
        views.WeekWithScheduleCalendar.as_view(),
        name='week_with_schedule'
    ),
    path('shop_config/',views.Shop_base_views.as_view(),name='shop_config'),
    path('shop_config/<int:shops_pk>/',views.Shop_base_views.as_view(),name='shop_config'),
    path('shift_csv/<int:shops_pk>/<int:year>/<int:month>/<int:day>/', views.Shift_csv.as_view(), name='shift_csv'),
    path('shift_csv/<int:shops_pk>/', views.Shift_csv.as_view(), name='shift_csv'),    
    # path('shop_config/',views.Shop_baseupdate_views.as_view(),name='shop_config'),
    # path('shop_config/<int:pk>/',views.Shop_baseupdate_views.as_view(),name='shop_config'),

    # path('shop_config/<int:pk>/',views.Shop_config_list.as_view(),name='shop_config_list'),
    path(
        'user/<int:user_pk>/month_with_schedule/',
        views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'
    ),
    path(
        'user/<int:user_pk>/month_with_schedule/<int:year>/<int:month>/',
        views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'
    ),
    path('user/<int:user_pk>/mycalendar/', views.MyCalendar.as_view(), name='mycalendar'),
    path(
        'user/<int:user_pk>/mycalendar/<int:year>/<int:month>/<int:day>/', views.MyCalendar.as_view(), name='mycalendar'
    ),
    path(
        'user/<int:user_pk>/month_with_forms/',
        views.MonthWithFormsCalendar.as_view(), name='month_with_forms'
    ),
    path(
        'user/<int:user_pk>/month_with_forms/<int:year>/<int:month>/<int:day>/',
        views.MonthWithFormsCalendar.as_view(), name='month_with_forms'
    ),
        path(
        'day_config/<int:shop_pk>/',
        views.Shop_config_day_views.as_view(), name='day_config'
    ),
    path(
        'day_config/<int:shop_pk>/<int:year>/<int:month>/<int:day>/',
        views.Shop_config_day_views.as_view(), name='day_config'
    ),

]
