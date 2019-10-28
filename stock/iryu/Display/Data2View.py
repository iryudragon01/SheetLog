from account_control.models import UserStart
from stock.models import Item, LogSheet,TempExpense,TopUp,Income,Expense,DisplayLogSheet
from django.utils import timezone
from account_control.iryu.user_start_script import User_Start_Handle


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
        worker = UserStart.objects.get(username=request.user)
        log_sheet_starts = LogSheet.objects.filter(version=worker.version_log)
        log_sheet_ends = LogSheet.objects.filter(version=LogSheet.objects.last().version)
        top_ups = TopUp.objects.filter(date_log__gt=worker.date_log)
        items = Item.objects.all()
        ####delete old Log sheet display
        DisplayLogSheet.objects.all().delete()
        for item in items:
            start_log= DisplayLogSheet(item=item, value=0, type=1)
            for log_sheet_start in log_sheet_starts:
                if log_sheet_start.item==item:
                    start_log.value=log_sheet_start.Last_stock
            start_log.save()
        for item in items:
            end_log= DisplayLogSheet(item=item, value=0, type=2)
            for log_sheet_end in log_sheet_ends:
                if log_sheet_end.item==item:
                    start_log.value=log_sheet_end.Last_stock
            end_log.save()




        content = {
            'start_rows': DisplayLogSheet.objects.filter(type=1),
            'end_rows': DisplayLogSheet.objects.filter(type=2),
        }
        return content

    #  End get display

#get topup



































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





