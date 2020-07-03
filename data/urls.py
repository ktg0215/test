from django.urls import path
from . import views

app_name = 'data'
urlpatterns = [

    path('upload/', views.upload, name='upload'),
    path('data_list/', views.Datalist.as_view(), name='data_list'),

]