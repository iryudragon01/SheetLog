from account_manager.models import User_Start
from stock.models import LogSheet,TopUp,TempExpense,Income,Expense


class User_Start_Handle:
    def user_superior(self,request):
        users = User_Start.objects.all()
        for user in users:
            if user.user_superior>User_Start.objects.get(username=request.user).user_superior:
                self.edit_user_start(self,user)

    def edit_user_start(self, user):
        log_sheet=LogSheet.objects.last()
        user.version_log = log_sheet.version
        user.date_log = log_sheet.date_log
        user.version_temp = TempExpense.objects.all().count()
        user.version_top_up = TopUp.objects.all().count()
        user.version_income = Income.objects.all().count()
        user.version_expense = Expense.objects.all().count()
        user.save()


