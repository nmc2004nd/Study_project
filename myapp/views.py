from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, SubjectSerializer, LessonSerializer, AssignmentSerializer, ReferenceSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Subject, Lesson, Assignment, Reference

from django.shortcuts import get_object_or_404

# Nên dùng khi giao tiếp ngoài 
# Viết độc lập các API endpoint
# @api_view(['POST'])
# def register_user(request):
#     serializer = UserRegistrationSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(
#             {"message": "User created successfully. Please login to continue.", 
#              "infor": serializer.data},
#             status=status.HTTP_201_CREATED
#         )
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Nên dùng trong giao tiếp nội bộ
class UserRegistrationView(APIView):
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully. Please login to continue.", 
                 "infor": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SubjectListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(teacher=request.user)  # teacher = user hiện tại
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        subject = get_object_or_404(Subject, pk=pk)
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)

    def put(self, request, pk):
        subject = get_object_or_404(Subject, pk=pk)
        serializer = SubjectSerializer(subject, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subject = get_object_or_404(Subject, pk=pk)
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class LessonListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_id):
        lessons = Lesson.objects.filter(subject_id=subject_id)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

    def post(self, request, subject_id):
        subject = get_object_or_404(Subject, pk=subject_id)
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(subject=subject)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_id, pk):
        lesson = get_object_or_404(Lesson, pk=pk, subject_id=subject_id)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

    def put(self, request, subject_id, pk):
        lesson = get_object_or_404(Lesson, pk=pk, subject_id=subject_id)
        serializer = LessonSerializer(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subject_id, pk):
        lesson = get_object_or_404(Lesson, pk=pk, subject_id=subject_id)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    

class AssignmentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_id, lesson_id):
        assignments = Assignment.objects.filter(lesson_id=lesson_id, lesson__subject_id=subject_id)
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)

    def post(self, request, subject_id, lesson_id):
        lesson = get_object_or_404(Lesson, pk=lesson_id, subject_id=subject_id)
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(lesson=lesson)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignmentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_id, lesson_id, pk):
        assignment = get_object_or_404(Assignment, pk=pk, lesson_id=lesson_id, lesson__subject_id=subject_id)
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data)

    def put(self, request, subject_id, lesson_id, pk):
        assignment = get_object_or_404(Assignment, pk=pk, lesson_id=lesson_id, lesson__subject_id=subject_id)
        serializer = AssignmentSerializer(assignment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subject_id, lesson_id, pk):
        assignment = get_object_or_404(Assignment, pk=pk, lesson_id=lesson_id, lesson__subject_id=subject_id)
        assignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Reference Views
class ReferenceListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_id):
        references = Reference.objects.filter(subject_id=subject_id)
        serializer = ReferenceSerializer(references, many=True)
        return Response(serializer.data)

    def post(self, request, subject_id):
        subject = get_object_or_404(Subject, pk=subject_id)
        serializer = ReferenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(subject=subject)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReferenceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_id, pk):
        reference = get_object_or_404(Reference, pk=pk, subject_id=subject_id)
        serializer = ReferenceSerializer(reference)
        return Response(serializer.data)

    def put(self, request, subject_id, pk):
        reference = get_object_or_404(Reference, pk=pk, subject_id=subject_id)
        serializer = ReferenceSerializer(reference, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subject_id, pk):
        reference = get_object_or_404(Reference, pk=pk, subject_id=subject_id)
        reference.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)