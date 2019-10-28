from django.urls import path
from stock.iryu.Item import views as item_views
from stock.iryu.Top_up import views as top_up_views
from stock.iryu.Display import views as display_views
app_name = 'stock'
urlpatterns=[
    # Display
    path('',display_views.IndexView,name='index'),


    # Item
    path('item/create/',item_views.CreateView,name='itemcreate'),
    path('item/list/',item_views.ListView,name='itemlist'),
    path('item/edit/<int:pk>/',item_views.EditView,name='itemedit'),

    # topup
    path('topup/',top_up_views.Top_up_View,name='topup'),
    path('topup/list/',top_up_views.Top_up_List_View,name='topup_list'),
    path('topup/edit/<int:pk>',top_up_views.Top_up_Edit_View,name='topup_edit'),

]