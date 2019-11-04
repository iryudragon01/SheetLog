from django.shortcuts import render, redirect
from stock.models import Item
from account_control.models import UserStart
from . import Data2View
from .function import calculater
from stock.forms import InputTest
from django.utils import timezone


def IndexView(request):
    end_retrieve = timezone.now()
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
    content = {}
    if request.user.is_authenticated:
        worker = UserStart.objects.get(username=request.user)
        content['start_date'] = worker.date_log.strftime('%m/%d/%Y %I:%M %p')
        content['end_date'] = timezone.localtime(timezone.now()).strftime('%m/%d/%Y %I:%M %p')
        print(timezone.localtime(timezone.now()),'timezone now')

    if request.POST:
        result = calculater.text2date(request)
        if result is not 'fail':
            content = result
            return render(request,'stock/display/index.html',content)
        else:
            content['errors'] = result
    return render(request,'stock/display/getdate.html',content)
