from django.urls import path
from . import views

app_name = 'register'

urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('top/',views.Top.as_view(),name='top'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user_create/', views.register_user, name='user_create'),
    path('index/',views.Tem.as_view(),name='index'),
    path('user_list/',views.Userlist.as_view(),name='user_list'),
    path('user_list/<int:pk>/shop_list/',views.Shoplist.as_view(),name='shop_list'),
    path('<int:pk>/delete/',views.UserDelete.as_view(),name='user_delete'),
   ]
