from stock.models import Item,TopUp
from django.utils import timezone
from account_control.models import UserStart

class data2view:
    def top_up(self,request):
        items = Item.objects.filter(type=3)
        current_time = timezone.now()
        print('hello for item',items.count())
        for item in items:
            new_top_up = TopUp(
                item=item,
                volume=request.POST.get(item.name),
                worker=request.user,
                date_log=current_time)
            new_top_up.save()
            print(new_top_up.item.name,'   volume  ', new_top_up.value)

    def edit(self,request,pk):
        if 'DELETE' in request.POST:
            del_top_up = TopUp.objects.get(id=pk)
            del_top_up.delete()
        else:
            update_top_up = TopUp.objects.get(id=pk)
            update_top_up.volume = int(request.POST.get('volume'))
            update_top_up.save()

    def list(self,request):
        worker=UserStart.objects.get(username=request.user)
        top_ups = TopUp.objects.filter(date_log__gt=worker.date_log)
        content = {'top_ups': top_ups}
        return content
