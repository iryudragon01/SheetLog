from stock.models import Income, Expense, TempExpense
from django.db.models import Sum


def getstatement(start_date,end_date):
    content = {}
    sum_income = 0
    sum_expense = 0
    sum_temp = 0
    if Income.objects.filter(date_log__gt=start_date,date_log__lt=end_date):
        content['incomes'] = Income.objects.filter(date_log__gt=start_date,date_log__lt=end_date)
        sum_income = Income.objects.filter(date_log__gt=start_date,date_log__lt=end_date).aggregate(Sum('value'))['value__sum']
    else:
        content['incomes'] = []
    if Expense.objects.filter(date_log__gt=start_date,date_log__lt=end_date):
        content['expenses'] = Expense.objects.filter(date_log__gt=start_date,date_log__lt=end_date)
        sum_expense = Expense.objects.filter(date_log__gt=start_date,date_log__lt=end_date).aggregate(Sum('value'))['value__sum']

    else:
        content['expenses'] = []
    if TempExpense.objects.filter(date_log__gt=start_date,date_log__lt=end_date):
        content['temps'] = TempExpense.objects.filter(date_log__gt=start_date,date_log__lt=end_date)
        sum_temp = TempExpense.objects.filter(date_log__gt=start_date,date_log__lt=end_date).aggregate(Sum('value'))['value__sum']

    else:
        content['temps'] = []
    content['sum_income'] = sum_income
    content['sum_expense'] = sum_expense
    content['sum_temp'] = sum_temp
    return content
