from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from .models import UserProfile, Course, Application
from .forms import RegistrationForm, LoginForm, ApplicationForm, ReviewForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('my_applications')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            UserProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone']
            )
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('my_applications')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field != '__all__':
                        messages.error(request, f'{error}')
    else:
        form = RegistrationForm()
    
    return render(request, 'courses/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('my_applications')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('my_applications')
            else:
                messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    
    return render(request, 'courses/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('login')

@login_required
def home_view(request):
    courses = Course.objects.all()
    return render(request, 'courses/home.html', {'courses': courses})

@login_required
def create_application_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Заявка успешно создана и направлена на рассмотрение')
            return redirect('my_applications')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = ApplicationForm()
    
    courses = Course.objects.all()
    return render(request, 'courses/create_application.html', {'form': form, 'courses': courses})

@login_required
def my_applications_view(request):
    applications = request.user.applications.all().order_by('-created_at')
    return render(request, 'courses/my_applications.html', {'applications': applications})

@login_required
def submit_review_view(request, application_id):
    application = get_object_or_404(Application, id=application_id, user=request.user)
    
    if application.status == 'completed' and not application.review:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                application.review = form.cleaned_data['review']
                application.review_created = timezone.now()
                application.save()
                messages.success(request, 'Спасибо за ваш отзыв!')
            else:
                messages.error(request, 'Ошибка при добавлении отзыва')
    
    return redirect('my_applications')