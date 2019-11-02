from django.shortcuts import render, redirect
from stock.models import Item
from account_control.models import UserStart
from . import Data2View


# Create your views here.
def IndexView(request):
    if not request.user.is_authenticated:
        return redirect('account_control:index')
    # if login check if item Exist
    # check if login with admin
    elif UserStart.objects.filter(username=request.user).count() == 0:
        return redirect('account_control:logout')
    else:
        if request.POST:  # if Post Update data
            content = Data2View.setdisplay(request)
            return render(request,'stock/display/index.html',content)

        else:  # login and get view list
            if Item.objects.all().count() == 0:
                return redirect('stock:create_item')  # send to create item
            else:
                content = Data2View.getdisplay(request)
                return render(request, 'stock/display/index.html', content)
