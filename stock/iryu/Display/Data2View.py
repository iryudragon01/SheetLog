from account_control.models import UserStart
from stock.models import Item, LogSheet, TempExpense, TopUp, Income, Expense, DisplayLogSheet, DisplayTopUp
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

        #get_top_up = self.gettopup(self, worker=worker, top_ups=top_ups,logsheet=log_sheet_start)
        content = {'items': zip(DisplayLogSheet.objects.filter(type=1), DisplayLogSheet.objects.filter(type=2)),
                   'top_ups': {} #get_top_up
                   }
        return content

    #  End get display

    # get topup
    def gettopup(self, worker, top_ups,logsheet):
        # Claer DisplayDate and DisplayTopUp table
        DisplayTopUp.objects.all().delete()

        items = Item.objects.filter(type=3)
        index = 2
        for item in items:
            new_display = DisplayTopUp(item=item,row=1,date_log=worker.date_log)
            new_display.save()
            for sheet in  LogSheet.objects.filter(version=worker.version_log):
                if sheet.item==new_display.item:
                    new_display.value=sheet.value
                    new_display.save()
        if top_ups.count()>0:
            last_version = top_ups.last().version
            for row in range(last_version+1):
                if top_ups.filter(version=row).count()>0:
                    for item in items:
                        new_display = DisplayTopUp(item=item,row=index,date_log=timezone.now())
                        new_display.save()
                        for top_up in top_ups:
                            if top_up.version==row and top_up.item==new_display.item:
                                new_display.value=top_up.value
                                new_display.date_log=top_up.date_log
                                new_display.save()

                    index += 1






        top_up_list = []
        for row in range(int(DisplayTopUp.objects.all().count()/items.count())+1):
            if row==0:
                sub_list=['name']
                for item in items:
                    sub_list.append(item.name)
                top_up_list.append(sub_list)
            else:
                sub_list = [DisplayTopUp.objects.get(item=item,row=row).date_log]
                for top_up in DisplayTopUp.objects.filter(row=row):
                    sub_list.append(top_up.value)
                top_up_list.append(sub_list)

        return top_up_list

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
