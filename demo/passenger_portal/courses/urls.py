from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-application/', views.create_application_view, name='create_application'),
    path('my-applications/', views.my_applications_view, name='my_applications'),
    path('submit-review/<int:application_id>/', views.submit_review_view, name='submit_review'),
]