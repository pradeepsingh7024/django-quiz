# views.py using DRF ViewSets (custom, not ModelViewSet)
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import QuestionPaper, Question, Answer

from .serializers import (
    UserSerializer,
    QuestionPaperSerializer,
    QuestionSerializer,
    AnswerSerializer,
    UserRegisterSerializer
)

class LoginView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]  # <- ADD THIS

    def create(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "username": user.username,
                "message": "Login successful"
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class UserRegisterViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        data = request.data
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            user = User(
                username=serializer.validated_data['username'],
                email=serializer.validated_data.get('email', '')
            )
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionPaperViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = QuestionPaper.objects.all()
        serializer = QuestionPaperSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        paper = QuestionPaper(
            title=data.get('title', ''),
            description=data.get('description', '')
        )
        paper.save()
        serializer = QuestionPaperSerializer(paper)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        paper = QuestionPaper.objects.filter(pk=pk).first()
        if not paper:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionPaperSerializer(paper)
        return Response(serializer.data)

    def update(self, request, pk=None):
        paper = QuestionPaper.objects.filter(pk=pk).first()
        if not paper:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        paper.title = data.get('title', paper.title)
        paper.description = data.get('description', paper.description)
        paper.save()
        serializer = QuestionPaperSerializer(paper)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        paper = QuestionPaper.objects.filter(pk=pk).first()
        if not paper:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        paper.delete()
        return Response({'message': 'Deleted successfully'})

class QuestionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = Question.objects.all()
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        question = Question(
            paper_id=data.get('paper'),
            question_text=data.get('question_text', ''),
            question_type=data.get('question_type', 'MCQ'),
            option1=data.get('option1', ''),
            option2=data.get('option2', ''),
            option3=data.get('option3', ''),
            option4=data.get('option4', ''),
            correct_option=data.get('correct_option', '')
        )
        question.save()
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        question = Question.objects.filter(pk=pk).first()
        if not question:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def update(self, request, pk=None):
        question = Question.objects.filter(pk=pk).first()
        if not question:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        question.question_text = data.get('question_text', question.question_text)
        question.question_type = data.get('question_type', question.question_type)
        question.option1 = data.get('option1', question.option1)
        question.option2 = data.get('option2', question.option2)
        question.option3 = data.get('option3', question.option3)
        question.option4 = data.get('option4', question.option4)
        question.correct_option = data.get('correct_option', question.correct_option)
        question.save()
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        question = Question.objects.filter(pk=pk).first()
        if not question:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        question.delete()
        return Response({'message': 'Deleted successfully'})

class AnswerViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = Answer.objects.filter(user=request.user)
        serializer = AnswerSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        answer = Answer(
            user=request.user,
            question_id=data.get('question'),
            answer_text=data.get('answer_text', ''),
            is_correct=data.get('is_correct', False),
            checked=data.get('checked', False)
        )
        answer.save()
        serializer = AnswerSerializer(answer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        answer = Answer.objects.filter(pk=pk, user=request.user).first()
        if not answer:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)

    def update(self, request, pk=None):
        answer = Answer.objects.filter(pk=pk, user=request.user).first()
        if not answer:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        answer.answer_text = data.get('answer_text', answer.answer_text)
        answer.is_correct = data.get('is_correct', answer.is_correct)
        answer.checked = data.get('checked', answer.checked)
        answer.save()
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        answer = Answer.objects.filter(pk=pk, user=request.user).first()
        if not answer:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        answer.delete()
        return Response({'message': 'Deleted successfully'})
