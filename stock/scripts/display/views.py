from django.shortcuts import render, redirect
from stock.models import Item
from account_control.models import UserStart
from . import Data2View
from .function import calculater
from datetime import datetime
from stock.forms import InputTest


def IndexView(request):
    end_retrieve = datetime.now()
    if not request.user.is_authenticated:
        return redirect('account_control:index')
    # if login check if item Exist
    # check if login with admin
    elif UserStart.objects.filter(username=request.user).count() == 0:
        return redirect('account_control:logout')
    else:
        if request.POST:  # if Post Update data
            content = Data2View.setdisplay(request)
            return render(request, 'stock/display/index.html', content)

        else:  # login and get view list
            if Item.objects.all().count() == 0:
                return redirect('stock:create_item')  # send to create item
            else:
                content = calculater.normal_get_log(request)
                return render(request, 'stock/display/index.html', content)


def getDateView(request):
    form = InputTest()
    content = {
        'form': form
    }

    if request.POST:
        result = calculater.text2date(request)
        if result is not 'fail':
            content = result
            return render(request,'stock/display/index.html',content)
        else:
            content['errors']=result
    return render(request,'stock/display/getdate.html',content)
