from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from .models import Question
from django.contrib.auth.decorators import login_required
from .models import Submission
from django.db import IntegrityError
from .models import Choice
from datetime import datetime
from django.utils import timezone
from .models import Test

def index(request):
    return render(request, 'assessment/index.html')


@login_required
def test(request, test_type_id):
    now = timezone.now()
    total_test_duration = 60  # e.g., 15 minutes

    test_type = get_object_or_404(Test, type_id=test_type_id)

    # Check if the user has a completed submission for this test
    completed_submission = Submission.objects.filter(user=request.user, test=test_type, completed=True).first()
    if completed_submission:
        # Show the results if the test is already completed
        print('Completed')
        return redirect('assessment:results')

    # Check for an ongoing test
    ongoing_submission = Submission.objects.filter(user=request.user, test=test_type, completed=False).first()
    if ongoing_submission:
        elapsed_time = (now - ongoing_submission.start_time).total_seconds()
        remaining_time = max(total_test_duration - elapsed_time, 0)

        if elapsed_time > total_test_duration:
            # Time limit exceeded
            return redirect('assessment:submit')

        questions = Question.objects.filter(test=test_type)
        return render(request, 'assessment/test.html', {
            'questions': questions,
            'remaining_time': remaining_time
        })

    # Start a new test if no submission exists
    Submission.objects.create(user=request.user, test=test_type, total=Question.objects.count(), start_time=now)
    questions = Question.objects.filter(test=test_type)
    return render(request, 'assessment/test.html', {
        'questions': questions,
        'remaining_time': total_test_duration
    })

@login_required
def submit(request):
    submission = Submission.objects.filter(user=request.user, completed=False).first()
    if submission:
        if request.method == 'POST':
            score = 0
            questions = Question.objects.all()
            for question in questions:
                selected_choice = request.POST.get(f'question_{question.id}')
                if selected_choice:
                    try:
                        correct_choice = question.choice_set.get(is_correct=True)
                        if str(correct_choice.id) == selected_choice:
                            score += 1
                    except Choice.DoesNotExist:
                        pass
            total = questions.count()
            
            # Update the submission
            submission.score = score
            submission.total = total
            submission.completed = True
            submission.save()

            return render(request, 'assessment/submit.html')
        else:
            # Handle case where form is not submitted (e.g., page refresh after time expired)
            return redirect('assessment:time_expired')
    else:
        return redirect('assessment:home')

    

@login_required
def results(request):
    # Fetch all submissions for the current user
    user_submissions = Submission.objects.filter(user=request.user).order_by('-start_time')
    
    return render(request, 'assessment/results.html', {'submissions': user_submissions})


def admin(request):
    return render(request, 'assessment/admin.html')

def sign_in(request):
    if request.user.is_authenticated:
        # Check if the user has already taken the test
        if Submission.objects.filter(user=request.user, completed=True).exists():
            # User has taken the test, redirect to results
            return redirect('assessment:results')
        else:
            # User hasn't taken the test, redirect to test
            return redirect('assessment')

    # Existing sign-in logic
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('assessment:home')
        else:
            return render(request, 'assessment/index.html', {'form': 'Your username and password didn\'t match.'})
    else:
        return render(request, 'assessment/index.html')


@login_required
def home(request):
    # Fetch all available tests
    tests = Test.objects.all()
    # Get the current user
    current_user = request.user
    return render(request, 'assessment/home.html', {'tests': tests, 'user': current_user})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assessment:sign_in')  # Redirect to the sign-in page after successful registration
        else:
            return render(request, 'assessment/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'assessment/register.html', {'form': form})
    
def time_expired(request):
    return render(request, 'assessment/time_expired.html')
