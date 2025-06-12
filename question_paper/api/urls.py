# urls.py
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from .api_views import (
    UserRegisterViewSet,
    QuestionPaperViewSet,
    QuestionViewSet,
    AnswerViewSet,
    LoginView
)
###### api  url ####
router = DefaultRouter()
router.register('register', UserRegisterViewSet, basename='register')
router.register('papers', QuestionPaperViewSet, basename='questionpaper')
router.register('questions', QuestionViewSet, basename='question')
router.register('answers', AnswerViewSet, basename='answer')
router.register('login',LoginView,basename='login')
###### api  url ####

urlpatterns = [
    path('api/', include(router.urls)),

    ###### template file  url ####
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('solve/<int:pk>/', views.solve_paper, name='solve_paper'),
    path('submit/<int:pk>/', views.submit_answers, name='submit_answers'),
    path('result/<int:pk>/', views.view_result, name='result'),
    ###### template file  url ####
]
