from django.shortcuts import render, redirect
from stock.models import Item, DateTimeTemplate
from account_control.models import UserStart
from . import Data2View
from datetime import datetime
from django.views.generic import CreateView


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
                content = Data2View.getdisplay(request, end_retrieve)
                return render(request, 'stock/display/index.html', content)


class getDateTimeView(CreateView):
    model = DateTimeTemplate
    fields = ['date', 'time']
    template_name = 'stock/display/getdate.html'

    def form_valid(self, form):
        print('hello',form.cleaned_data)

        return redirect('stock:getenddate')
