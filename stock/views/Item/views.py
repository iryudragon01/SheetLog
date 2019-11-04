from django.shortcuts import render, redirect
from stock.models import Item
from stock.views.Item.Data2View import create,edit
from account_control.scripts.script import is_superior


def CreateView(request):
    if not is_superior(request):
        return redirect('account_control:permit_denied')
    content = {}
    if request.method == 'POST':
        makenewitem = create(request)
        content['createnewitem'] = makenewitem
    return render(request, 'stock/Item/create.html', content)


def ListView(request):
    content = {
        'items': Item.objects.all()
    }

    return render(request, 'stock/Item/list.html', content)


def EditView(request, pk=None):
    if not is_superior(request):
        return redirect('account_control:permit_denied')
    if id is not None:
        if request.POST:
            edit(request, pk)
        elif Item.objects.filter(id=pk).count() == 1:
            content = {'item': Item.objects.get(id=pk) }
            return render(request, 'stock/Item/edit.html', content)
    return redirect('stock:list_item')
