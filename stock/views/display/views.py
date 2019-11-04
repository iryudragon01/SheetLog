from django.shortcuts import render, redirect
from stock.models import Item
from account_control.models import UserStart
from . import Data2View
from .function import calculater
from django.utils import timezone
from account_control.scripts import script


def IndexView(request):
    script.account_permit(request)    # check user permit before do other thing
    if request.POST:  # if Post Update data
        if 'startdate' in request.POST:
            content = calculater.text2date(request)
            return render(request, 'stock/display/index.html', content)
        else:
            content = Data2View.setdisplay(request)
            return render(request, 'stock/display/index.html', content)

    else:  # login and get view list
        if Item.objects.all().count() == 0:
            return redirect('stock:create_item')  # send to create item
        else:
            content = calculater.normal_get_log(request)
            worker = UserStart.objects.get(username=request.user)
            content['start_date'] = worker.date_log.strftime('%m/%d/%Y %I:%M %p')
            content['end_date'] = timezone.localtime(timezone.now()).strftime('%m/%d/%Y %I:%M %p')
            return render(request, 'stock/display/index.html', content)


