from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from .defined import *

# Create your models here.
class CustomUser(AbstractUser):
    # Bạn có thể thêm các trường tùy chỉnh cho người dùng tại đây
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username
    

class Subject(models.Model):

    name = models.CharField(max_length=100, verbose_name="Tên môn học")
    code = models.CharField(max_length=10, verbose_name="Mã môn học")
    credits = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Số tín chỉ")
    subject_type = models.CharField(max_length=20, choices=APP_VALUE_SUBJECT_TYPE_CHOICES, default='general', verbose_name="Loại môn học")
    description = models.TextField(blank=True, verbose_name="Mô tả môn học")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE,verbose_name= "Giảng viên phụ trách" ,related_name='subjects')
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, verbose_name="Điều kiện tiên quyết", related_name='prerequisite_subjects')
    is_active = models.BooleanField(default=True, verbose_name = "Trạng thái hoạt động")

    class Meta:
        verbose_name = "Môn học"
        verbose_name_plural = "Môn học"
        ordering = ['code']

    def __str__(self):
        return f"{self.name} ({self.code})"
    

class Lesson(models.Model):

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Môn học", related_name='lessons')
    title = models.CharField(max_length=200, verbose_name="Tiêu đề bài học")
    lesson_number = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Số thứ tự bài học")
    lesson_type = models.CharField(max_length=20, choices=APP_VALUE_LESSON_TYPE_CHOICES, default='theory', verbose_name="Loại bài học")
    content = models.TextField(verbose_name="Nội dung bài học")
    video_url = models.URLField(blank=True, null=True, verbose_name="URL video bài học")

    class Meta:
        verbose_name = "Bài học"
        verbose_name_plural = "Bài học"
        ordering = ['subject', 'lesson_number'] 

    def __str__(self):
        return f"{self.subject.name} - Bài {self.lesson_number}: {self.title}"
    

class Assignment(models.Model):

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Bài học", related_name='assignments')
    title = models.CharField(max_length=200, verbose_name="Tiêu đề bài tập")
    description = models.TextField(verbose_name="Mô tả bài tập")
    due_date = models.DateTimeField(verbose_name="Hạn nộp bài tập")
    assignment_type = models.CharField(max_length=20, choices=APP_VALUE_ASSIGNMENT_TYPE_CHOICES, default='homework', verbose_name="Loại bài tập")

    class Meta:
        verbose_name = "Bài tập"
        verbose_name_plural = "Bài tập"
        ordering = ['lesson', 'due_date']

    def __str__(self):
        return f"{self.lesson.subject.name} - {self.title}"
    
class Reference(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Môn học", related_name='references')
    title = models.CharField(max_length=200, verbose_name="Tiêu đề tài liệu")
    url = models.URLField(verbose_name="URL tài liệu")
    description = models.TextField(blank=True, verbose_name="Mô tả tài liệu")

    class Meta:
        verbose_name = "Tài liệu tham khảo"
        verbose_name_plural = "Tài liệu tham khảo"
        ordering = ['subject', 'title']

    def __str__(self):
        return f"{self.subject.name} - {self.title}"