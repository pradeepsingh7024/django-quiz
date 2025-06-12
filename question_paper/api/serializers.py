# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import QuestionPaper, Question, Answer

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class QuestionPaperSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)

    def create(self, validated_data):
        paper = QuestionPaper(
            title=validated_data['title']
        )
        paper.save()
        return paper

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance

class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    paper = serializers.PrimaryKeyRelatedField(queryset=QuestionPaper.objects.all())
    question_text = serializers.CharField()
    question_type = serializers.CharField()
    option1 = serializers.CharField(allow_blank=True, required=False)
    option2 = serializers.CharField(allow_blank=True, required=False)
    option3 = serializers.CharField(allow_blank=True, required=False)
    option4 = serializers.CharField(allow_blank=True, required=False)
    correct_option = serializers.CharField(allow_blank=True, required=False)

    def create(self, validated_data):
        question = Question(
            paper=validated_data['paper'],
            question_text=validated_data['question_text'],
            question_type=validated_data['question_type'],
            option1=validated_data.get('option1', ''),
            option2=validated_data.get('option2', ''),
            option3=validated_data.get('option3', ''),
            option4=validated_data.get('option4', ''),
            correct_option=validated_data.get('correct_option', '')
        )
        question.save()
        return question

    def update(self, instance, validated_data):
        instance.paper = validated_data.get('paper', instance.paper)
        instance.question_text = validated_data.get('question_text', instance.question_text)
        instance.question_type = validated_data.get('question_type', instance.question_type)
        instance.option1 = validated_data.get('option1', instance.option1)
        instance.option2 = validated_data.get('option2', instance.option2)
        instance.option3 = validated_data.get('option3', instance.option3)
        instance.option4 = validated_data.get('option4', instance.option4)
        instance.correct_option = validated_data.get('correct_option', instance.correct_option)
        instance.save()
        return instance

class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    answer_text = serializers.CharField()
    is_correct = serializers.BooleanField(required=False)
    checked = serializers.BooleanField(required=False)

    def create(self, validated_data):
        answer = Answer(
            user=self.context['request'].user,
            question=validated_data['question'],
            answer_text=validated_data['answer_text'],
            is_correct=validated_data.get('is_correct', False),
            checked=validated_data.get('checked', False)
        )
        answer.save()
        return answer

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)
        instance.answer_text = validated_data.get('answer_text', instance.answer_text)
        instance.is_correct = validated_data.get('is_correct', instance.is_correct)
        instance.checked = validated_data.get('checked', instance.checked)
        instance.user = self.context['request'].user
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

