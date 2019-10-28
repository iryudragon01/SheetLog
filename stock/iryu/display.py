from account_manager.models import User_Start
from stock.models import Item, LogSheet,TempExpense,TopUp,Income,Expense
from django.utils import timezone
from account_manager.iryu.user_start_script import User_Start_Handle
from stock.iryu.Top_up_link import Top_up_work


class Display:
    def getdisplay(self, request):
        content = {'account_manager': request.user}
        all_item = Item.objects.all()

        # create log sheet if not exist
        if LogSheet.objects.all().count() == 0:
            for item in all_item:
                new_log_sheet = LogSheet(item=item,
                                         version=1,
                                         Last_stock=0,  # stock last value
                                         date_log=timezone.now(),
                                         start_log_version=1,
                                         end_log_version=1)
                new_log_sheet.save()
        # retrieve data from log sheet
        user = User_Start.objects.get(username=request.user)
        log_sheet_starts = LogSheet.objects.filter(version=user.version_log)
        log_sheet_ends = LogSheet.objects.filter(version=LogSheet.objects.last().version)
        items_name = []
        items_first = []
        items_last = []
        items_price = []
        items_sale_volume = []
        items_money = []
        items_sum = []
        all_top_up = TopUp.objects.filter(date_log__gt=user.date_log)
        # fill up start log sheet with top up.
        for top_up in all_top_up:
            for log_sheet in log_sheet_starts:
                if log_sheet.item == top_up.item:
                    log_sheet.Last_stock += top_up.volume
        # set data to items
        for log_sheet, log_sheet_end in zip(log_sheet_starts, log_sheet_ends):
            items_name.append(log_sheet.item.name)
            items_price.append(log_sheet.item.price)
            if log_sheet.item.type == 1:
                items_first.append(log_sheet.Last_stock)
                items_last.append(log_sheet_end.Last_stock)
                items_sale_volume.append(log_sheet_end.Last_stock - log_sheet.Last_stock)
                items_money.append(log_sheet.item.price * (log_sheet_end.Last_stock - log_sheet.Last_stock))
            elif log_sheet.item.type == 2:
                items_first.append(0)
                items_last.append(log_sheet_end.Last_stock - log_sheet.Last_stock)
                items_sale_volume.append(log_sheet_end.Last_stock - log_sheet.Last_stock)
                items_money.append(log_sheet.item.price * (log_sheet_end.Last_stock - log_sheet.Last_stock))
            else:
                items_first.append(log_sheet.Last_stock)
                items_last.append(log_sheet_end.Last_stock)
                items_sale_volume.append(log_sheet.Last_stock - log_sheet_end.Last_stock)
                items_money.append(log_sheet.item.price * (log_sheet.Last_stock - log_sheet_end.Last_stock))

            # sum items
        sum_money = 0
        for money in items_money:
            sum_money += money
            items_sum.append(sum_money)

        items = zip(items_name, items_first, items_last, items_price, items_sale_volume, items_money, items_sum)

        content['items'] = items
        content['top_ups'] = Top_up_work.get_top_up(Top_up_work,request)
        return content

    #  End get display
    # start set display
    def setdisplay(self, request):
        items = Item.objects.all()
        log_sheet_last = LogSheet.objects.last()
        current_time = timezone.now()
        worker = User_Start.objects.get(username=request.user)
        for item in items:
            new_log_sheet = LogSheet(item=item,
                                     version=log_sheet_last.version + 1,
                                     Last_stock=request.POST.get(item.name),
                                     date_log=current_time,
                                     start_log_version=worker.version_log,
                                     end_log_version=log_sheet_last.version)
            new_log_sheet.save()

        User_Start_Handle.user_superior(User_Start_Handle,request)    # update account_manager start
        return self.getdisplay(self, request)





