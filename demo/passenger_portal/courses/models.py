from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', message='Формат: 8(XXX)XXX-XX-XX')],
        verbose_name='Телефон'
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название курса')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'Идет обучение'),
        ('completed', 'Обучение завершено'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Предоплата по QR-коду'),
        ('transfer', 'Оплата картой МИР'),
        ('post', 'Постоплата в офисе организации')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    start_date = models.DateField(verbose_name='Дата начала обучения')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name='Способ оплаты')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    review = models.TextField(blank=True, null=True, verbose_name='Отзыв')
    review_created = models.DateTimeField(blank=True, null=True, verbose_name='Дата отзыва')

    def __str__(self):
        return f'{self.user.username} - {self.course.name}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'