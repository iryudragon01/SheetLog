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

def edit(request):
    id = request.POST['temp_id']
    value = request.POST['value']
    if value == '':
        return 'Amount is not valid'
    if int(value) <0:
        return 'Amount is not valid'
    if 'DELETE' in request.POST:
        TempExpense.objects.get(id=id).delete()
        return 'deleted'
    else:
        update = TempExpense.objects.get(id=id)
        update.value = int(value)
        update.save()
        return 'updated'