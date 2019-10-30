from django.shortcuts import redirect,render
from .create import create
from account_control.models import UserStart
from stock.models import TempExpense

def CreateView(request):
    content = {}
    if request.POST:
        result = create(request)
        if result == 'success':
            return redirect('stock:list_temp')
        else:
            content['message'] = result
    return render(request,'stock/temp/create.html',content)


def ListView(request):
    worker = UserStart.objects.get(username=request.user)
    data = TempExpense.objects.filter(date_log__gt=worker.date_log)
    content ={
        'temps': data
    }
    return render(request,'stock/temp/list_temp.html',content)


def EditView(request,pk):

    return render(request,'stock/temp/edit_temp.html')