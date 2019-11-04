from stock.models import Item,TopUp
from datetime import datetime
from django.utils.datetime_safe import datetime
from account_control.models import UserStart


def top_up(request):
    items = Item.objects.filter(type=3)
    save_time = datetime.now()
    top_up_version = 1
    if TopUp.objects.all().count() > 0:
        top_up_version = TopUp.objects.last().version + 1
    for item in items:
        new_top_up = TopUp(
            item=item,
            value=request.POST.get(item.name),
            worker=request.user,
            date_log=save_time,
            version=top_up_version
        )
        if int(new_top_up.value) > 0:
            new_top_up.save()


def edit(request, pk):
    if 'DELETE' in request.POST:
        del_top_up = TopUp.objects.get(id=pk)
        del_top_up.delete()
    else:
        update_top_up = TopUp.objects.get(id=pk)
        update_top_up.value = int(request.POST.get('value'))
        update_top_up.save()


def list(request):
    worker = UserStart.objects.get(username=request.user)
    top_ups = TopUp.objects.filter(date_log__gt=worker.date_log)
    content = {'top_ups': top_ups}
    return content

    