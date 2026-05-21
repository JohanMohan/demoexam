from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Application

# форма регистрации с валидацией

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        min_length=6,
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[RegexValidator(regex=r'^[a-zA-Z0-9]+$', message='Только латиница и цифры')]
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Подтверждение пароля'
    )
    full_name = forms.CharField(
        label='ФИО',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[RegexValidator(regex=r'^[а-яА-ЯёЁ\s]+$', message='Только кириллица и пробелы')]
    )
    phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '8(999)123-45-67'}),
        validators=[RegexValidator(regex=r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', message='Формат: 8(XXX)XXX-XX-XX')]
    )
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# логирование ошибок
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        import re
        if not re.match(r'^[а-яА-ЯёЁ\s]+$', full_name):
            raise forms.ValidationError('ФИО должно содержать только буквы кириллицы и пробелы')
        if len(full_name.strip()) < 5:
            raise forms.ValidationError('ФИО должно содержать минимум 5 символов')
        return full_name.strip()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        import re
        if not re.match(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', phone):
            raise forms.ValidationError('Телефон должен быть в формате: 8(XXX)XXX-XX-XX')
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data

# форма логина

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class ApplicationForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'ДД.ММ.ГГГГ'}),
        input_formats=['%d.%m.%Y'],
        label='Дата начала обучения'
    )

    class Meta:
        model = Application
        fields = ['course', 'start_date', 'payment_method']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'payment_method': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }

    def clean_start_date(self):
        from datetime import date
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date < date.today():
            raise forms.ValidationError('Дата начала обучения не может быть в прошлом')
        return start_date

#класс отзывов
class ReviewForm(forms.Form):
    review = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        label='Ваш отзыв'
    )