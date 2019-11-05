from django.shortcuts import render, redirect
from stock.models import Item
from account_control.models import UserStart
from .function import calculater,data2view
from django.utils import timezone
from account_control.scripts import script


def IndexView(request):
    if not script.account_permit(request):  # check user permit before do other thing
        return redirect('account_control:logout')
    if request.POST:  # if Post Update data
        if 'startdate' in request.POST:
            content = calculater.text2date(request)
            return render(request, 'stock/display/index.html', content)
        else:
            content = data2view.setdisplay(request)
            return render(request, 'stock/display/index.html', content)

    else:  # login and get view list
        if Item.objects.all().count() == 0:
            return redirect('stock:create_item')  # send to create item
        else:
            content = calculater.normal_get_log(request)
            return render(request, 'stock/display/index.html', content)


