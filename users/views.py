from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse



def logout_view(request):
    logout(request)
    return render(request, 'learning_logs/index.html') 

def register(request):
    if request.method != 'POST':
        reg_form = UserCreationForm()
    else:
        reg_form = UserCreationForm(request.POST)
        if reg_form.is_valid():
            new_user = reg_form.save()
            auth_user = authenticate(username = new_user.username, password = request.POST['password1'])
            login(request, auth_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))
    context = {'reg_form' : reg_form}
    return render(request, 'users/register.html', context)
