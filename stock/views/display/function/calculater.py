from datetime import datetime
from stock.models import LogSheet
from django.db.models import Sum,Min,Max
from account_control.models import UserStart
from django.utils import timezone
from . import data2view


def volume_sale(item,start,end):
    if item.type == 1:
        return end-start
    elif item.type == 2:
        return end
    else:
        return start-end


def item_money(item,start,end):
    return item.price*volume_sale(item,start,end)


def text2date(request):
    plain_start = request.POST['startdate']
    plain_end = request.POST['enddate']
    start_date = datetime.strptime(plain_start,'%m/%d/%Y %I:%M %p')
    end_date = datetime.strptime(plain_end,'%m/%d/%Y %I:%M %p')
    start_log = LogSheet.objects.filter(date_log__gt=start_date).aggregate(Min('version'))['version__min']
    end_log = LogSheet.objects.filter(date_log__lt=end_date).aggregate(Max('version'))['version__max']
    if end_date>start_date:
        log_sheets_start = LogSheet.objects.filter(version=start_log)
        log_sheets_end = LogSheet.objects.filter(version=end_log)
        content = data2view.getdisplay(log_sheets_start,log_sheets_end,end_date)
        content['start_date']=start_date.strftime('%m/%d/%Y %I:%M %p')
        content['end_date'] = end_date.strftime('%m/%d/%Y %I:%M %p')
        return content
    else:
        return 'fail'


def normal_get_log(request):
    worker = UserStart.objects.get(username=request.user)
    log_sheets_start = LogSheet.objects.filter(version=worker.version_log)
    log_sheets_end = LogSheet.objects.filter(
        version=LogSheet.objects.filter(date_log__lt=timezone.now()).last().version)
    end_statement_date = timezone.now()
    return data2view.getdisplay(log_sheets_start,log_sheets_end,end_statement_date)

