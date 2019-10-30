from account_control.models import UserStart
from stock.models import Income,Expense
def getstatement(start_date):

    if Income.objects.filter(date_log__gt=start_date).count()>0:
        print('hello from inside')
        income = Income.objects.filter(date_log__gt=start_date)
        expense = Expense.objects.filter(date_log__gt=start_date)
        return {'incomes': income,'expenses': expense}