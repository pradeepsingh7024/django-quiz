from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm
from .models import QuestionPaper, Question, Answer
from django.contrib.auth.decorators import login_required

def register_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_student = True
        user.save()
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=uname, password=pwd)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


@login_required
def dashboard(request):
    papers = QuestionPaper.objects.all()
    return render(request, 'dashboard.html', {'papers': papers})


@login_required
def solve_paper(request, pk):
    paper = get_object_or_404(QuestionPaper, id=pk)
    questions = paper.question_set.all()

    # Attach options list for template iteration
    for q in questions:
        q.options = [q.option1, q.option2, q.option3, q.option4]

    return render(request, 'solve_paper.html', {
        'questions': questions,
        'paper': paper
    })


@login_required
def submit_answers(request, pk):
    paper = get_object_or_404(QuestionPaper, id=pk)
    questions = paper.question_set.all()

    for question in questions:
        user_answer = request.POST.get(str(question.id), "").strip()
        is_mcq = question.question_type == "MCQ"
        is_correct = user_answer == question.correct_option if is_mcq else False

        Answer.objects.create(
            user=request.user,
            question=question,
            answer_text=user_answer,
            is_correct=is_correct,
            checked=is_mcq
        )

    return redirect('result', pk=paper.id)


@login_required
def view_result(request, pk):
    answers = Answer.objects.filter(user=request.user, question__paper__id=pk)
    score = answers.filter(is_correct=True).count()
    return render(request, 'result.html', {'answers': answers, 'score': score})


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')
