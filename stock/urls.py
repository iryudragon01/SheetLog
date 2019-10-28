from django.urls import path
from stock import views

app_name = 'stock'
urlpatterns={
    path('',views.test,name='index')
}