from django.shortcuts import render
def CreateView(request):
    content = {}
    return render(request,'stock/statement/create.html',content)