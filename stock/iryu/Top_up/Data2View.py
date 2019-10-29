from stock.models import Item,TopUp
from datetime import datetime
from django.utils.datetime_safe import datetime
from account_control.models import UserStart

class data2view:
    def top_up(self,request):
        items = Item.objects.filter(type=3)
        save_time = datetime.now()
        top_up_version=1
        if TopUp.objects.all().count()>0:
            top_up_version=TopUp.objects.last().version+1
        for item in items:
            new_top_up = TopUp(
                item=item,
                value=request.POST.get(item.name),
                worker=request.user,
                date_log=save_time,
                version=top_up_version
            )
            new_top_up.save()

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
