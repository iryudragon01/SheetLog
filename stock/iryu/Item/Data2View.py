from stock.models import Item


class data2view:
    def create(self, request):
        itemexist = Item.objects.filter(name=request.POST.get('name')).count()
        if itemexist == 0:
            newitem = Item(name=request.POST.get('name'),
                           price=int(request.POST.get('price')),
                           type=int(request.POST.get('type')),
                           )
            newitem.save()
            return 'success'
        return 'Item is exist'

    def edit(self, request, pk):
        if 'DELETE' in request.POST:
            del_item = Item.objects.get(id=pk)
            del_item.delete()
        else:
            update_item = Item.objects.get(id=pk)
            update_item.price = request.POST.get('price')
            update_item.type = request.POST.get('type')
            update_item.save()
