from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm

# Create your views here.


def register_account(req):
    if req.user.is_authenticated:
        return redirect('books:home')

    form = CreateUserForm()

    if req.method == 'POST':
        form = CreateUserForm(req.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            return redirect('user_auth:login')

    context = {
        'form': form,
    }

    return render(req, 'registration/register.html', context)


def login_account(req):
    if req.user.is_authenticated:
        return redirect('books:home')

    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(req, user)
            return redirect('books:home')

    return render(req, 'registration/login.html')


def logout_account(req):
    logout(req)
    return redirect('user_auth:login')
