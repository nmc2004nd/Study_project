from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    # Thêm các URL khác nếu cần
    path('login/', TokenObtainPairView.as_view(), name='user_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('subjects/', views.SubjectListCreateView.as_view(), name='subject-list-create'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject-detail'),

    # LESSON (thuộc về subject)
    path('subjects/<int:subject_id>/lessons/', views.LessonListCreateView.as_view(), name='lesson-list-create'),
    path('subjects/<int:subject_id>/lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson-detail'),

      # Assignment URLs
    path('subjects/<int:subject_id>/lessons/<int:lesson_id>/assignments/', 
         views.AssignmentListCreateView.as_view(), name='assignment-list-create'),
    path('subjects/<int:subject_id>/lessons/<int:lesson_id>/assignments/<int:pk>/',
         views.AssignmentDetailView.as_view(), name='assignment-detail'),

    # Reference URLs
    path('subjects/<int:subject_id>/references/',
         views.ReferenceListCreateView.as_view(), name='reference-list-create'),
    path('subjects/<int:subject_id>/references/<int:pk>/',
         views.ReferenceDetailView.as_view(), name='reference-detail'),
]
