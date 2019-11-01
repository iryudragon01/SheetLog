
from django.urls import path
from . import  views

app_name = 'account_control'

urlpatterns = [

    path('', views.LoginView, name='index'),
    path('register/',views.RegisterView,name='register'),
    path('logout',views.LogoutView,name='logout'),
    path('reset/data/index',views.ResetIndexView,name='reset_index')
]
