from django.urls import  path
from . import views
from stock.iryu.Item import views as item_views
from stock.iryu.Top_up import views as top_up_views
from stock.iryu.Display import views as display_views
from stock.iryu.statement import views as statement_views
from stock.iryu.temp import views as temp_views
app_name='stock'
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

    # statement
    path('create_statement/',statement_views.CreateView,name='create_statement'),
    path('list_income/',statement_views.ListIncomeView,name='list_income'),
    path('edit_income/<int:pk>/',statement_views.EditIncomeView,name='edit_income'),
    path('list_expense/',statement_views.ListExpenseView,name='list_expense'),
    path('edit_expense/<int:pk>/',statement_views.EditExpenseView,name='edit_expense'),

    # temp expense
    path('temp_create/',temp_views.CreateView,name='create_temp'),
    path('list_temp/',temp_views.ListView,name='list_temp'),
    path('edit_temp/<int:pk>',temp_views.EditView,name='edit_temp'),

]