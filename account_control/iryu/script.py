from account_control.models import UserStart
from stock.models import LogSheet


def user_superior(request, hard_mode=0):
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




