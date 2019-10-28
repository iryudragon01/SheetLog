from account_control.models import UserStart
from stock.models import LogSheet,TopUp,TempExpense,Income,Expense


class User_Start_Handle:
    def user_superior(self,request):
        users = UserStart.objects.all()
        for user in users:
            if user.user_superior>UserStart.objects.get(username=request.user).user_superior:
                self.edit_user_start(self,user)

    def edit_user_start(self, user_row):
        if LogSheet.objects.all().count()==0:
            user_row.version_log = 0
        else:
            log_sheet=LogSheet.objects.last()
            user_row.version_log = log_sheet.version
            user_row.date_log = log_sheet.date_log
            user_row.save()


