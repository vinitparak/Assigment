from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, EmployeeRegistration, EmployeeLogin, EmployeeData
from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from .models import Users, Employee
from django.core.mail import EmailMessage
from django.core.mail import send_mail
import random
import string

# Create your views here.
def home(request):

    if request.COOKIES.get('email', None) is not None:
        return redirect('company_view')
    elif request.COOKIES.get('id', None) is not None:
        id = request.COOKIES.get('id')
        emp = Employee.objects.get(id=id)
        if emp.type == '0':
            return redirect('manager_view')
        else:
            return redirect('employee', company_id=emp.company_id.id, employee_id = id)

    return render(request, 'home.html', {})


def register(request):

    invalid = False

    if request.method == 'GET':
        form = RegisterForm()

    elif request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.password = make_password(form.cleaned_data['password'])
            # print(is_password_usable(user.password))
            if Users.objects.filter(email = user.email).count() == 1:
                invalid = True
            else:
                user.save()
                return redirect('company_login')
        else:
            form = RegisterForm()
            invalid = True

    return render(request, 'register.html', {'form': form, 'invalid': invalid})


def company_login(request):

    invalid = False

    if request.method == 'GET':
        form = LoginForm()

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        print(request.POST)
        print()
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            count = Users.objects.filter(email=email).count()
            if count == 0:
                invalid = True
            else:
                user = Users.objects.get(email=email)
                if check_password(password, user.password):
                    response = redirect('company_view')
                    response.set_cookie('email', user.email)
                    return response
                else:
                    invalid = True
        else:
            invalid = True
            form = RegisterForm()

    return render(request, 'company_login.html', {'form': form, 'invalid': invalid})


def company_view(request):

    if request.COOKIES.get('email', None) is None:
        return redirect('company_login')

    invalid = False
    exist = False
    if request.method == "GET":
        form = EmployeeRegistration()

    elif request.method == "POST":
        form = EmployeeRegistration(request.POST, request.FILES)

        print([(field.label, field.errors) for field in form])

        if form.is_valid():
            employee = form.save(commit=False)
            employee.company_id = Users.objects.get(email=request.COOKIES.get('email'))
            employee.email = form.cleaned_data['email']
            if Employee.objects.filter(email = employee.email).count() == 1:
                exist = True
            else:
                employee.name = form.cleaned_data['name']
                employee.phone = form.cleaned_data['phone']
                employee.gender = form.cleaned_data['gender']
                employee.type = form.cleaned_data['type']
                employee.hobbies = form.cleaned_data['hobbies']
                employee.profile_picture = form.cleaned_data['profile_picture']
                password = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(5))
                employee.password = make_password(password)
                send_mail(employee.email, password)
                employee.save()
        else:
            invalid = True
    return render(request, 'company_view.html', {'form': form, 'invalid': invalid, 'exist': exist})


def logout(request):

    val = 'email'
    if request.COOKIES.get(val, None) is None:
        val = 'id'
    response = redirect('home')
    response.delete_cookie(val)
    return response


def employee_login(request):



    invalid = False
    exist = False
    if request.method == "GET":
        form = EmployeeLogin()
    if request.method == "POST":
        form = EmployeeLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            count = Employee.objects.filter(email=email).count()
            if count == 0:
                invalid = True
            else:
                user = Employee.objects.get(email=email)
                if check_password(password, user.password):
                    if user.type == '0':
                        response = redirect('manager_view')
                    else:
                        response = redirect('employee', company_id=user.company_id.id, employee_id=user.id)
                    response.set_cookie('id', user.id)
                    return response
                else:
                    invalid = True
        else:
            invalid = True
            form = RegisterForm()

    return render(request, 'employee_login.html', {'form': form, 'invalid': invalid})


def manager_view(request):

    if request.COOKIES.get('id', None) is None:
        redirect('home')

    manager = Employee.objects.get(id=request.COOKIES.get('id'))
    if manager.type == '1':
        return redirect('employee', company_id = manager.company_id.id, employee_id = manager.id)
    id = manager.company_id
    employees = Employee.objects.filter(company_id=id)

    return render(request, 'manager_view.html', {'employees': employees})


def employee(request, company_id, employee_id):

    id = int(request.COOKIES.get('id', None))
    # print(type(id), type(employee_id))
    if id is None:
        redirect('home')
    if id != employee_id:
        manager = Employee.objects.get(id=id)
        # print('asdf', manager.type)
        if manager.type == '1':
            return redirect('home')
    employee = Employee.objects.get(id = employee_id)
    if employee.company_id.id != company_id:
        return redirect('home')

    if request.method == "POST":
        if request.FILES.get('profile_picture', None) is None:
            request.FILES['profile_picture'] = employee.profile_picture
        form = EmployeeData(request.POST, request.FILES)
        print([(field.label, field.errors) for field in form])
        if form.is_valid():
            employee.name = form.cleaned_data['name']
            print(form.cleaned_data['name'], employee.name)
            employee.phone = form.cleaned_data['phone']
            employee.gender = form.cleaned_data['gender']
            employee.hobbies = form.cleaned_data['hobbies']
            employee.profile_picture = form.cleaned_data['profile_picture']
            employee.save()

    initial ={
        'name': employee.name,
        'phone': employee.phone,
        'email': employee.email,
        'gender': employee.gender,
        'hobbies': employee.hobbies,
        'profile_picture': employee.profile_picture
    }

    form = EmployeeData(initial = initial)
    return render(request, 'employee.html', {'form': form})


def send_mail(email, password):
    email = EmailMessage('Credentials', 'Username: {0}\nPassword: {1}'.format(email, password), to=[email])
    email.send()