from stock.models import Item, TopUp, LogSheet
from django.utils import timezone
from account_manager.models import User_Start


class Top_up_work:
    def create(self, request):
        currenttime = timezone.now()
        allitem = Item.objects.filter(type=3)
        if allitem:
            for item in allitem:
                newitem = TopUp(item=item, volume=request.POST.get(item.name), worker=request.POST.get('worker'),
                                date_log=currenttime)
                newitem.save()

    def get_top_up(self, request):
        if TopUp.objects.all().count() > 0:
            worker = User_Start.objects.get(username=request.user)
            log_sheet = LogSheet.objects.filter(version=worker.version_log)
            all_top_up = TopUp.objects.filter(date_log__gt=worker.date_log)
            items = Item.objects.filter(type=3)
            date_logs = []
            top_ups = []

            date_logs.append('name')
            date_logs.append(log_sheet[0].date_log)
            names = []
            log_sheet_first = []
            for item in items:
                names.append(item.name)
                for log in log_sheet:
                    if log.item == item:
                        log_sheet_first.append(log.Last_stock)
            top_ups.append(names)
            top_ups.append(log_sheet_first)

            for index in range(int(all_top_up.count() / items.count())):
                top_up = []
                for loop in range(items.count()):
                    top_up.append(all_top_up[index * items.count() + loop].volume)
                    if loop == items.count()-1:
                        print('hello')
                        date_logs.append(all_top_up[loop + items.count() * index].date_log)
                        top_ups.append(top_up)

            return zip(top_ups, date_logs)

        # end get Top Up
        # set Top up

    def set_top_up(self, request):
        items = Item.objects.filter(type=3)
        current_time = timezone.now()
        for item in items:
            new_top_up = TopUp(item=item,
                               volume=request.POST.get(item.name),
                               worker=request.user,
                               date_log=current_time
                               )
            new_top_up.save()
        return
