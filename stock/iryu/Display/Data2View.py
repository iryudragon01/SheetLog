from account_control.models import UserStart
from stock.models import Item, LogSheet, TempExpense, TopUp, Income, Expense, DisplayLogSheet,DisplayTopUp,DisplayDate
from django.utils import timezone
from account_control.iryu.user_start_script import User_Start_Handle


class Display:
    def getdisplay(self, request):
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
            start_log = DisplayLogSheet(item=item, value=0, type=1)
            for log_sheet_start in log_sheet_starts:
                if log_sheet_start.item == item:
                    start_log.value = log_sheet_start.value
            start_log.save()
        for item in items:
            end_log = DisplayLogSheet(item=item, value=0, type=2)
            for log_sheet_end in log_sheet_ends:
                if log_sheet_end.item == item:
                    start_log.value = log_sheet_end.value
            end_log.save()

        for top_up in top_ups:
            for display_log_sheet in DisplayLogSheet.objects.filter(type=1):
                if top_up.item == display_log_sheet.item:
                    display_log_sheet.value += top_up.value
                    display_log_sheet.save()

        get_topup=self.gettopup(self,request=request,worker=worker,items=items,top_ups=top_ups)
        content = {'items': zip(DisplayLogSheet.objects.filter(type=1), DisplayLogSheet.objects.filter(type=2))}

        return content

    #  End get display

    # get topup
    def gettopup(self,request,worker,items,top_ups):
        content = {}
        DisplayDate.objects.all().delete()
        index=2
        for item in items:
            DisplayTopUp(item=item, value=0, row=1, date_log=worker.date_log).save()

        for top_up in top_ups:
            if DisplayDate.objects.filter(date_log =top_up.date_log).count()==0:
                new_display_date = DisplayDate(date_log=top_up.date_log,row=index)
                new_display_date.save()
                index += 1

        for display_date in DisplayDate.objects.all():
            for item in items:
                if TopUp.objects.filter(date_log=display_date.date_log,item=item).count()==1:
                    DisplayTopUp(item=item,
                                 value=TopUp.objects.get(date_log=display_date.date_log,item=item).value,
                                 row=display_date.row,
                                 date_log=display_date.date_log
                                 ).save()
                else:
                    DisplayTopUp(item=item,value=0,row=display_date.row,date_log=display_date.date_log).save()







        return content
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