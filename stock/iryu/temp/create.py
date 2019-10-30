from stock.models import TempExpense
from django.utils import timezone
def create(request):
    name = request.POST['name']
    value = request.POST['value']
    if value == '' or name == '':
        return 'name and amount cannot be empty!!'
    elif int(value) <= 0:
        return 'amount format is wrong!!'
    TempExpense(name=name,value=value,date_log=timezone.now()).save()
    return 'success'
