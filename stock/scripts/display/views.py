from django.shortcuts import render, redirect
from stock.models import Item
from account_control.models import UserStart
from .Data2View import setdisplay,getdisplay


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
            content = setdisplay(request)
            return render(request,'stock/display/index.html',content)

        else:  # login and get view list
            if Item.objects.all().count() == 0:
                return redirect('stock:create_item')  # send to create item
            else:
                content = getdisplay( request)
                return render(request, 'stock/display/index.html', content)
