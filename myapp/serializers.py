from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Subject, Lesson, Assignment, Reference

# Lấy CustomUser đã tạo
User = get_user_model()


# ==== USER SERIALIZER ====
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        """
        Tạo user mới và tự hash password.
        """
        return User.objects.create_user(**validated_data)


# ==== SUBJECT SERIALIZER ====
class SubjectSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.username', read_only=True)

    class Meta:
        model = Subject
        fields = [
            'id', 'name', 'code', 'credits', 'subject_type', 'description',
            'teacher', 'teacher_name', 'prerequisites', 'is_active'
        ]


# ==== LESSON SERIALIZER ====
class LessonSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id', 'subject', 'subject_name', 'title',
            'lesson_number', 'lesson_type', 'content', 'video_url'
        ]
        read_only_fields = ['subject']
        extra_kwargs = {
            'title': {'required': True},
            'lesson_number': {'required': True, 'min_value': 1},
            'lesson_type': {'required': True},
            'content': {'required': True},
            'video_url': {'required': False, 'allow_null': True, 'allow_blank': True},
        }



# ==== ASSIGNMENT SERIALIZER ====
class AssignmentSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)

    class Meta:
        model = Assignment
        fields = [
            'id', 'lesson', 'lesson_title', 'title',
            'description', 'due_date', 'assignment_type'
        ]
        read_only_fields = ['lesson']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'due_date': {'required': True},
            'assignment_type': {'required': True},
        }


class ReferenceSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Reference
        fields = [
            'id', 'subject', 'subject_name', 'title',
            'url', 'description'
        ]
        read_only_fields = ['subject']
        extra_kwargs = {
            'title': {'required': True},
            'url': {'required': True},
            'description': {'required': False, 'allow_blank': True},
        }
