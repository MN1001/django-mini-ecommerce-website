from django.shortcuts import render ,redirect
from django.contrib.auth import login,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from . forms import RegForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def regview(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegForm
    return render(request,'registration/reg.html',{'form':form})

def loginview(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
        return redirect ('store:home')
    else:
        form = AuthenticationForm()
    return render(request,'registration/login.html',{'form':form})

@login_required
def logoutview(request):
    logout(request)
    return redirect('store:home')