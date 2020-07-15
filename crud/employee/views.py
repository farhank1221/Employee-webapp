from django.shortcuts import render, redirect
from employee.forms import EmployeeForm
from employee.models import Employee
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('show')
    else:
        form = RegisterForm()

        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'You are in our records now')
                return redirect('login')

        context = {'form': form}
        return render(request, "register/register.html", context)


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/show')
        else:
            messages.info(request, 'incorrect info')

    context = {}
    return render(request, "register/login.html", context)

@login_required(login_url='login')
def emp(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/show')
            except:
                pass
    else:
        form = EmployeeForm()
    return render(request, 'index.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def show(request):
    employees = Employee.objects.all()
    return render(request, "show.html", {'employees': employees})

@login_required(login_url='login')
def edit(request, id):
    employee = Employee.objects.get(id=id)
    return render(request, 'edit.html', {'employee': employee})

@login_required(login_url='login')
def update(request, id):
    employee = Employee.objects.get(id=id)
    form = EmployeeForm(request.POST, instance=employee)
    if form.is_valid():
        form.save()
        return redirect("/show")
    return render(request, 'edit.html', {'employee': employee})
#to delete the record
@login_required(login_url='login')
def destroy(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect("/show")
