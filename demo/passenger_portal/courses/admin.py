from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Course, Application

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'get_full_name', 'is_staff']
    search_fields = ['username', 'email', 'userprofile__full_name']
    
    def get_full_name(self, obj):
        return obj.userprofile.full_name if hasattr(obj, 'userprofile') else ''
    get_full_name.short_description = 'ФИО'

# настройки панели администратора 

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'course', 'start_date', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'course', 'payment_method', 'created_at']
    search_fields = ['user__username', 'user__userprofile__full_name', 'course__name']
    list_editable = ['status']
    list_per_page = 15
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Информация о заявке', {
            'fields': ('user', 'course', 'start_date', 'payment_method', 'status')
        }),
        ('Отзыв', {
            'fields': ('review', 'review_created'),
            'classes': ('collapse',)
        }),
    )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Course)
admin.site.register(Application, ApplicationAdmin)