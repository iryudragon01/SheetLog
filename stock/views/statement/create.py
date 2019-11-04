from stock.models import Income, Expense
from django.utils import timezone


def create(request):
    name = request.POST['name']
    value = request.POST['value']
    record_type = request.POST['record_type']
    result = {}
    if value == '' or name == '':
        result['message'] = 'name and amount cannot be empty!!'
        return result
    elif int(value) <= 0:
        return {'message': 'amount format is wrong!!'}
    if record_type == '1':
        Income(name=name, value=value, date_log=timezone.now()).save()
        return 'success-income'
    elif record_type == '2':
        Expense(name=name, value=value, date_log=timezone.now()).save()
        return 'success-expense'
    else:
        result['message'] = 'select type'
    return result


def edit(request):
    id = request.POST['income_id']
    value = request.POST['value']
    if value == '':
        return 'Amount is not valid'
    if int(value) < 0:
        return 'Amount is not valid'
    if 'DELETE' in request.POST:
        Income.objects.get(id=id).delete()
        return 'deleted'
    else:
        update = Income.objects.get(id=id)
        update.value = int(value)
        update.save()
        return 'updated'


def editexpense(request):
    id = request.POST['expense_id']
    value = request.POST['value']
    if value == '':
        return 'Amount is not valid'
    if int(value) < 0:
        return 'Amount is not valid'
    if 'DELETE' in request.POST:
        Expense.objects.get(id=id).delete()
        return 'deleted'
    else:
        update = Expense.objects.get(id=id)
        update.value = int(value)
        update.save()
        return 'updated'
