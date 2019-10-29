from account_control.models import UserStart
from stock.models import Item, LogSheet, TempExpense, TopUp, Income, Expense, DisplayLogSheet, DisplayTopUp
from django.utils import timezone
from account_control.iryu.user_start_script import User_Start_Handle
from django.db.models import Sum


class Display:
    def getdisplay(self, request):
        DictLog = {}
        ListFirst = []
        ListEnd = []
        all_item = Item.objects.all()

        # create log sheet if not exist
        if LogSheet.objects.all().count() == 0:
            for item in all_item:
                new_log_sheet = LogSheet(item=item,
                                         version=1,
                                         value=0,  # stock last value
                                         date_log=timezone.now())
                new_log_sheet.save()
        # retrieve data from log sheet
        worker = UserStart.objects.get(username=request.user)
        log_sheet_starts = LogSheet.objects.filter(version=worker.version_log)
        log_sheet_ends = LogSheet.objects.filter(version=LogSheet.objects.last().version)
        top_ups = TopUp.objects.filter(date_log__gt=worker.date_log)
        items = Item.objects.all()
        # delete old Log sheet display
        DisplayLogSheet.objects.all().delete()
        for item in items:
            sheet_start = 0
            sheet_end = 0
            if log_sheet_starts.filter(item=item).count() == 1:
                sheet_start = log_sheet_starts.get(item=item).value
            if item.type==3:
                item_top_ups = TopUp.objects.filter(item=item,date_log__gt=worker.date_log).aggregate(Sum('value'))
                sum_top_up = item_top_ups['value__sum']
                sheet_start += int(sum_top_up)
            ListFirst.append(sheet_start)
            if log_sheet_ends.filter(item=item).count() == 1:
                sheet_end=log_sheet_ends.get(item=item).value
            ListEnd.append(sheet_end)

        get_top_up = self.gettopup(self, worker=worker, top_ups=top_ups,logsheet=log_sheet_starts)
        content = {'items': zip(items,ListFirst,ListEnd),
                   'top_ups': get_top_up
                   }
        return content

    #  End get display

    # get topup
    def gettopup(self, worker, top_ups,logsheet):

        ListTop = []
        items = Item.objects.filter(type=3)
        list_row = ['name']
        for name in items:
            list_row.append(name.name)
        ListTop.append(list_row)
        list_sheet = ['date']
        for getvalue in items:
            sheet=0
            if logsheet.filter(item=getvalue).count() == 1:
                sheet = logsheet.get(item=getvalue).value
            list_sheet.append(sheet)
        ListTop.append(list_sheet)

        top_last=top_ups.last().version

        for loop in range(top_last):
            if top_ups.filter(version=loop).count()>0:
                row_top=top_ups.filter(version=loop)
                top_data=['']
                for item in items:
                    data_item = 0
                    if row_top.filter(item=item).count()==1:
                        data_item = row_top.get(item=item).value
                        top_data[0] = row_top.get(item=item).date_log
                    top_data.append(data_item)
                ListTop.append(top_data)




        return ListTop

    # start set display
    def setdisplay(self, request):
        items = Item.objects.all()
        log_sheet_last = LogSheet.objects.last()
        current_time = timezone.now()
        worker = UserStart.objects.get(username=request.user)
        for item in items:
            new_log_sheet = LogSheet(item=item,
                                     version=log_sheet_last.version + 1,
                                     value=request.POST.get(item.name),
                                     date_log=current_time)
            new_log_sheet.save()

        User_Start_Handle.user_superior(User_Start_Handle, request)  # update account_manager start
        return self.getdisplay(self, request)
