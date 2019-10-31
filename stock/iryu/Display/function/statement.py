from stock.models import Income, Expense, TempExpense


def getstatement(start_date):
    content = {}
    if Income.objects.filter(date_log__gt=start_date):
        content['incomes'] = Income.objects.filter(date_log__gt=start_date)
    else:
        content['incomes'] = []
    if Expense.objects.filter(date_log__gt=start_date):
        content['expenses'] = Expense.objects.filter(date_log__gt=start_date)
    else:
        content['expenses'] = []
    if TempExpense.objects.filter(date_log__gt=start_date):
        content['temps'] = TempExpense.objects.filter(date_log__gt=start_date)
    else:
        content['temps'] = []

    return content
