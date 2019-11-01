from stock.scripts.display.function.calculater import volume_sale, item_money
from account_control.models import UserStart
from stock.models import Item, LogSheet, TopUp
from django.utils import timezone
from account_control.scripts.script import user_superior
from django.db.models import Sum
from .function.statement import getstatement


def getdisplay(request):
    ListFirst = []
    ListEnd = []
    ListVolume = []
    ListMoney = []
    ListSum = []
    Sum_temp = 0
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

    for item in items:
        sheet_start = 0
        sheet_end = 0
        if log_sheet_starts.filter(item=item).count() == 1:
            if item.type == 1:
                sheet_start = log_sheet_starts.get(item=item).value
            if item.type == 2:
                sheet_start = 0
            if item.type == 3:
                sheet_start = log_sheet_starts.get(item=item).value
        if item.type == 3:
            item_top_ups = TopUp.objects.filter(item=item, date_log__gt=worker.date_log).aggregate(Sum('value'))
            sum_top_up = item_top_ups['value__sum']
            if sum_top_up:
                sheet_start += int(sum_top_up)
            else:
                sheet_start += 0
        ListFirst.append(sheet_start)

        if log_sheet_ends.filter(item=item).count() == 1:
            if item.type == 2:
                if log_sheet_starts.filter(item=item):
                    if log_sheet_ends.get(item=item):
                        sheet_end = log_sheet_ends.get(item=item).value - log_sheet_starts.get(item=item).value
                else:
                    if log_sheet_ends.filter(item=item):
                        sheet_end = log_sheet_ends.get(item=item).value
            else:
                sheet_end = log_sheet_ends.get(item=item).value
        ListEnd.append(sheet_end)

        # call function from other file
        ListVolume.append(volume_sale(item, sheet_start, sheet_end))
        ListMoney.append(item_money(item, sheet_start, sheet_end))
        Sum_temp += item_money(item, sheet_start, sheet_end)
        ListSum.append(Sum_temp)
    statement = getstatement(worker.date_log)
    get_top_up = gettopup(top_ups=top_ups, logsheet=log_sheet_starts)
    is_display_reset = '0'
    if worker.user_superior == 1:
        is_display_reset = '1'

    content = {'items': zip(items, ListFirst, ListEnd, ListVolume, ListMoney, ListSum),
               'top_ups': get_top_up,
               'incomes': statement['incomes'],
               'expenses': statement['expenses'],
               'temps': statement['temps'],
               'is_Display_reset': is_display_reset,
               }
    Sum_temp = statement['sum_income'] + Sum_temp
    content['sum_income'] = Sum_temp
    Sum_temp = -statement['sum_expense'] + Sum_temp
    content['sum_expense'] = Sum_temp
    Sum_temp = -statement['sum_temp'] + Sum_temp
    content['sum_temp'] = Sum_temp

    return content


#  End get display

# get topup
def gettopup(top_ups, logsheet):
    ListTop = []
    items = Item.objects.filter(type=3)
    list_row = ['name']
    for name in items:
        list_row.append(name.name)
    ListTop.append(list_row)
    list_sheet = ['date']
    for getvalue in items:
        sheet = 0
        if logsheet.filter(item=getvalue).count() == 1:
            sheet = logsheet.get(item=getvalue).value
        list_sheet.append(sheet)
    ListTop.append(list_sheet)
    if not top_ups.last():  # check if top_up is exist ?
        return ListTop

    top_last = top_ups.last().version

    for loop in range(top_last + 1):
        if top_ups.filter(version=loop).count() > 0:
            row_top = top_ups.filter(version=loop)
            top_data = ['']
            for item in items:
                data_item = ''
                if row_top.filter(item=item).count() == 1:
                    data_item = row_top.get(item=item).value
                    top_data[0] = row_top.get(item=item).date_log  # .strftime("%d/%m/%y %H:%M")
                top_data.append(data_item)
            ListTop.append(top_data)
    return ListTop


# start set display
def setdisplay(request):
    items = Item.objects.all()
    log_sheet_last = LogSheet.objects.last()
    current_time = timezone.now()
    for item in items:
        new_log_sheet = LogSheet(item=item,
                                 version=log_sheet_last.version + 1,
                                 value=request.POST.get(item.name),
                                 date_log=current_time)
        new_log_sheet.save()

    user_superior(request)  # update account_manager start
    return getdisplay(request)

    