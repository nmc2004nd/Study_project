from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Subject, Lesson, Reference, Assignment

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'bio', 'profile_picture',
    #                                   'facebook', 'twitter', 'instagram', 'github')}),
    #     ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    #     ('Important dates', {'fields': ('last_login', 'date_joined')}),
    # )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'credits', 'subject_type', 'teacher', 'is_active')
    list_filter = ('subject_type', 'is_active', 'teacher', 'credits')
    search_fields = ('name', 'code', 'description')
    list_editable = ('is_active',)
    filter_horizontal = ('prerequisites',)
    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'credits', 'subject_type', 'teacher', 'is_active')
        }),
        ('Mô tả', {
            'fields': ('description',)
        }),
        ('Điều kiện tiên quyết', {
            'fields': ('prerequisites',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'lesson_number', 'lesson_type')
    list_filter = ('lesson_type', 'subject')
    search_fields = ('title', 'content')
    list_select_related = ('subject',)
    ordering = ('subject', 'lesson_number')
    fieldsets = (
        (None, {
            'fields': ('subject', 'title', 'lesson_number', 'lesson_type')
        }),
        ('Nội dung', {
            'fields': ('content', 'video_url')
        }),
    )


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'assignment_type', 'due_date')
    list_filter = ('assignment_type', 'due_date', 'lesson__subject')
    search_fields = ('title', 'description')
    list_select_related = ('lesson', 'lesson__subject')
    date_hierarchy = 'due_date'
    fieldsets = (
        (None, {
            'fields': ('lesson', 'title', 'assignment_type')
        }),
        ('Chi tiết', {
            'fields': ('description', 'due_date')
        }),
    )


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'url')
    list_filter = ('subject',)
    search_fields = ('title', 'description', 'url')
    list_select_related = ('subject',)
    fieldsets = (
        (None, {
            'fields': ('subject', 'title', 'url')
        }),
        ('Mô tả', {
            'fields': ('description',)
        }),
    )