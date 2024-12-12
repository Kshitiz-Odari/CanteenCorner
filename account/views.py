from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm
from home.models import Customer

def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Username or password incorrect")

    return render(request, "account/login.html")

def register_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(
                user=user,
                name=form.cleaned_data.get('username'),
                address='',
                email=user.email,
                phone_number=''
            )
            messages.success(request, f"{user.username} created successfully!")
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CreateUserForm()

    context = {"form": form}
    return render(request, "account/register.html", context)

def logout_user(request):
    logout(request)
    return redirect('login')
