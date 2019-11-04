from django.shortcuts import render,redirect
from stock.models import Income,Expense
from account_control.models import UserStart
from .create import create,edit,editexpense
from account_control.scripts.script import is_superior


def CreateView(request):
    if request.POST:
        result = create(request)
        if result == 'success-income':
            return redirect('stock:list_income')
        elif result == 'success-expense':
            return redirect('stock:list_expense')
        else:
            return render(request,'stock/statement/create.html',result)
    return render(request,'stock/statement/create.html')


def ListIncomeView(request):
    worker = UserStart.objects.get(username=request.user)
    income = Income.objects.filter(date_log__gt=worker.date_log)
    content = {'incomes': income}
    return render(request,'stock/statement/list_income.html',content)


def ListExpenseView(request):
    worker = UserStart.objects.get(username=request.user)
    expense = Expense.objects.filter(date_log__gt=worker.date_log)
    content = {'expenses': expense}
    return render(request,'stock/statement/list_expense.html',content)


def EditIncomeView(request,pk):
    if not is_superior(request):
        return redirect('account_control:permit_denied')
    income = Income.objects.get(id=pk)
    content = {'income': income}
    if Income.objects.filter(id=pk).count() == 0:
        return redirect('stock:list_income')
    if request.POST:
        result = edit(request)
        if result == 'updated' or result == 'deleted':
            return redirect('stock:list_income')
        else:
            content['message'] = result
    return render(request,'stock/statement/edit_income.html',content)


def EditExpenseView(request,pk):
    if not is_superior(request):
        return redirect('account_control:permit_denied')
    expense = Expense.objects.get(id=pk)
    content = {'expense': expense}
    if Expense.objects.filter(id=pk).count() == 0:
        return redirect('stock:list_expense')
    if request.POST:
        result = editexpense(request)
        if result == 'updated' or result == 'deleted':
            return redirect('stock:list_expense')
        else:
            content['message'] = result
    return render(request,'stock/statement/edit_expense.html',content)