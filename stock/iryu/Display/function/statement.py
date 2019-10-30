
from stock.models import Income,Expense,TempExpense
def getstatement(start_date):

    if Income.objects.filter(date_log__gt=start_date).count()>0:
        income = Income.objects.filter(date_log__gt=start_date)
        expense = Expense.objects.filter(date_log__gt=start_date)
        temp = TempExpense.objects.filter(date_log__gt=start_date)
        return {'incomes': income,'expenses': expense,'temps': temp}