from account_control.models import UserStart
from stock.models import LogSheet
from datetime import datetime,timedelta
from django.utils import timezone
from django.shortcuts import redirect

def is_superior(request):
    worker = UserStart.objects.get(username=request.user)
    if worker.user_superior == 1:
        return True
    else:
        return False


def user_superior(request, hard_mode=0):
    account_permit(request)
    users = UserStart.objects.all()
    worker = UserStart.objects.get(username=request.user)
    for user in users:
        if user.user_superior > worker.user_superior:
            edit_user_start(user)
        elif user.user_superior == worker.user_superior and hard_mode == 1:
            edit_user_start(user)


def edit_user_start(user_row):
    if LogSheet.objects.all().count() == 0:
        user_row.version_log = 0
    else:
        log_sheet = LogSheet.objects.last()
        user_row.version_log = log_sheet.version
        user_row.date_log = log_sheet.date_log
        user_row.save()


def account_permit(request):
    if not request.user.is_authenticated:
        return redirect('account_control:index')
    # if login check if item Exist
    # check if login with admin
    elif UserStart.objects.filter(username=request.user).count() == 0:
        return redirect('account_control:logout')
    worker = UserStart.objects.get(username=request.user)
    ten_minutes = timedelta(minutes=15)
    time_now = timezone.now()
    if worker.last_login+ten_minutes > time_now:
        worker.last_login=time_now
        worker.save()
        return
    else:
        return redirect('account_control:logout')
