from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone
from .models import UserStart
from stock.models import LogSheet
from account_control.iryu.script import user_superior, edit_user_start,is_superior


# Create your views here.

def RegisterView(request):
    content = {}
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)

            # set up User start date
            if LogSheet.objects.all().count() == 0:
                log_sheet_version = 1
            else:
                log_sheet_version = LogSheet.objects.last().version
            new_user = UserStart(username=username, date_log=timezone.now(), version_log=log_sheet_version)
            new_user.save()
            update_user = UserStart.objects.get(username=username)
            edit_user_start(update_user)
            return redirect('account_control:index')
        else:
            content['registration_form'] = form
            return render(request, 'account_control/register.html', content)

    else:
        form = UserCreationForm()
        content['registration_form'] = form
    content['submit_value'] = 'Sign Up'
    content['reload'] = 'stop'
    return render(request, 'account_control/register.html', content)


def LoginView(request):
    if request.user.is_authenticated:
        return redirect('stock:index')  # if authenticated redirect to stock

    content = {}
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('stock:index')
        else:
            form = AuthenticationForm(request.POST)
            content['registration_form'] = form
    else:
        form = AuthenticationForm()
        content['registration_form'] = form
    content['reload'] = 'stop'
    content['submit_value'] = 'Login'
    return render(request, 'account_control/register.html', content)


def LogoutView(request):
    logout(request)
    return redirect('account_control:index')


def ResetIndexView(request):
    if is_superior(request):
        user_superior(request, hard_mode=1)
        return redirect('stock:index')
    else:
        return redirect('account_control:permit_denied')

def AuthorityFailView(request):
    return render(request,'account_control/fail_authority.html')
