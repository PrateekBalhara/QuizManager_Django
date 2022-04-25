import random

from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.db.models import Avg, Max, Min, Sum
from .models import Quiz, Question, Result

NUMBER_OF_QUESTIONS_IN_THE_QUIZ = 5;

# Function to return Result message based on Score percent
def get_result_message(score):
    print("Get result message: " + str(score))
    if score==100:
        return "You are a genius!"
    elif score>=80:
        return "Excellent Work!"
    elif score>=60:
        return "Good Work!"
    else:
        return "Please try again!"


# View for homepage
def homepage(request):
    # Fetch all quiz topics
    quizes = Quiz.objects.all()
    for quiz in quizes:
        # Fetch Avg, Min and Max score for each quiz
        quiz.avg = Result.objects.filter(quiz_id = quiz.id).aggregate(Avg('score')).get('score__avg')
        quiz.max = Result.objects.filter(quiz_id=quiz.id).aggregate(Max('score')).get('score__max')
        quiz.min = Result.objects.filter(quiz_id=quiz.id).aggregate(Min('score')).get('score__min')
        if not quiz.avg:
            quiz.avg = 0
        if not quiz.max:
            quiz.max = 0
        if not quiz.min:
            quiz.min = 0
        quiz.avg = int(quiz.avg)
    # Render and return homepage
    return render(request, 'homepage.html', {'quizes': quizes})

# Return webpage to attempt quiz
def quiz(request, quiz_id):
    # In case of quiz submit
    if(request.method == "POST"):
        score = 0
        # Get all questions for current quiz topic
        questions = Question.objects.filter(quiz=quiz_id)
        for i in list(map(lambda question: question.id,questions)):
            # request.POST has dict with "quiz_id + i" as key and value as answer
            # { '1_1' : '1_2', '1_2': '2_2'}
            # Fetch question and answer key-value pair
            answer = request.POST.get(str(quiz_id) + "_" + str(i))
            if(answer):
                # If selected option matches answer then
                #  Score + 1
                if answer.split("_")[1] == answer.split("_")[2]:
                    score +=1
            else:
                print("Error!!!!")
        # Find Score percent
        score = score*100/min(len(questions), NUMBER_OF_QUESTIONS_IN_THE_QUIZ)
        # Save Result
        result = Result(quiz_id = quiz_id, user_id = 1, score=score )
        result.save()

        return render(request, 'result.html', {'message':get_result_message(score),
                                               'retake': True if score<50 else False,
                                               'quiz_id': quiz_id})
    else:
        # If request is get
        try:
            # Fetch all questions for quiz_id
            questions = Question.objects.filter(quiz=quiz_id)
            questions_to_be_asked = []
            # SELECT A RANDOM SAMPLE OF QUESTIONS
            sample = random.sample(range(1, len(questions) + 1), min(len(questions), NUMBER_OF_QUESTIONS_IN_THE_QUIZ))
            for i in sample:
                # Append randomly selected question to 'questions_to_be_asked' list
                questions_to_be_asked.append(questions[i-1:i][0])
            return render(request, 'quiz.html', {'quiz_id': quiz_id,
                                                 'questions': questions_to_be_asked,
                                                 })
        except Question.DoesNotExist:
            return  Http404



def results(request):
    # Fetch result for user
    result_queryset = Result.objects.filter(user_id = 1)
    return render(request, 'user_result.html', {'results': result_queryset})


# from django.shortcuts import render
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .forms import NewUserForm
#
# def login_request(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request=request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.info(request, f"You are now logged in as {username}")
#                 return redirect('/')
#             else:
#                 messages.error(request, "Invalid username or password.")
#         else:
#             messages.error(request, "Invalid username or password.")
#     form = AuthenticationForm()
#     return render(request = request,
#                   template_name = "../templates/login.html",
#                   context={"form":form})
#
# # def logout_request(request):
# #     logout(request)
# #     messages.info(request, "Logged out successfully!")
# #     return redirect("main:homepage")
#
#
# def register_request(request):
#     pass
#
# def homepage(request):
#     pass
#
