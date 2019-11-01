from django.shortcuts import render,redirect
from stock.models import Item,TopUp
from stock.iryu.Top_up.Data2View import data2view
from account_control.iryu.script import is_superior


def Top_up_View(request):
    content = {'items': Item.objects.filter(type=3)}
    if request.POST:
        data2view.top_up(data2view,request)
        return redirect('stock:list_top_up')
    return render(request, 'stock/top_up/create.html', content)


def Top_up_List_View(request):
    content=data2view.list(data2view,request)
    return render(request, 'stock/top_up/list.html',content)


def Top_up_Edit_View(request,pk):
    if not is_superior(request):
        return redirect('account_control:permit_denied')
    if TopUp.objects.filter(id=pk).count() == 1:
        if request.POST:
            data2view.edit(data2view,request,pk)
        else:
            content = {'top_up': TopUp.objects.get(id=pk)}
            return render(request, 'stock/top_up/edit.html', content)
    return redirect('stock:list_top_up')
