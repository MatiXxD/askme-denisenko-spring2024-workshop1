from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.models import Question, Answer, Tag
from django.http import Http404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from app.forms import LoginForm, RegistrationForm, SettingsForm, QuestionForm, AnswerForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required



def pagination(request, questions, per_page):
    page_num = request.GET.get("page", 1)
    paginator = Paginator(questions, per_page=per_page)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(1)
                
    return page_obj
    


def index(request):
    new_questions = Question.objects.new_questions()
    return render(request, template_name="index.html", 
                  context={"questions" : pagination(request, new_questions, 20),
                           "popular_tags": Tag.objects.popular_tags(20)})


def hot(request):
    hot_questions = Question.objects.hot_questions()
    return render(request, template_name="hot.html", 
                  context={"questions" : pagination(request, hot_questions, 20),
                           "popular_tags": Tag.objects.popular_tags(20)})

@csrf_protect
@login_required(redirect_field_name="continue")
def account_settings(request):
    user = request.user
    if request.method == "GET":
        form = SettingsForm()
    if request.method == "POST":
        form = SettingsForm(request.POST)
        if form.is_valid():
            form.save(user)
            return render(request, template_name="account_settings.html",
                          context={"popular_tags": Tag.objects.popular_tags(20),
                                   "form": form, "saved": 1})
                      
    return render(request, template_name="account_settings.html",
                  context={"popular_tags": Tag.objects.popular_tags(20),
                           "form": form, "saved": 0})


@csrf_protect
def log_in(request):
    if request.method == "GET":
        login_form = LoginForm()
    elif request.method == "POST":
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user:
                login(request, user)
                return redirect(request.GET.get("continue", "/"))
            else:
                login_form.add_error(None, "Wrong password or user does not exist.")
                login_form.makeInvalid()
        
    return render(request, template_name="login.html",
                  context={"popular_tags": Tag.objects.popular_tags(20), 
                           "login": login_form})


def log_out(request):
    logout(request)
    referer = request.META.get("HTTP_REFERER")
    return redirect(referer)


def registration(request):
    if request.method == "GET":
        user_form = RegistrationForm()
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                return redirect(reverse("index"))
            else:
                user_form.add_error(None, "User saving error!")
        
    return render(request, template_name="registration.html",
                  context={"popular_tags": Tag.objects.popular_tags(20),
                           "form": user_form})


def list_by_tag(request, tag):
    try:
        questions_by_tag = Question.objects.questions_by_tag(tag)
    except Question.DoesNotExist:
        raise Http404
    return render(request, template_name="list_by_tag.html",
                  context={"questions" : pagination(request, questions_by_tag, 20),
                           "tag" : tag,
                           "popular_tags": Tag.objects.popular_tags(20)})


@csrf_protect
@login_required(redirect_field_name="continue")
def new_question(request):
    user = request.user
    if request.method == "GET":
        form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(user)
            return redirect(reverse("question", args=[question.id]))      
        else:
            form.add_error(None, "Can't validate form")   

    return render(request, template_name="new_question.html",
                  context={"popular_tags": Tag.objects.popular_tags(20), "form": form})

@csrf_protect
def question(request, question_id):
    NUM_PER_PAGE = 5
    
    question = get_object_or_404(Question, id=question_id)
    user = request.user
    if request.method == "GET":
        form = AnswerForm()
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(user, question)
            answers = Answer.objects.question_answers(question_id)
            answer_index = list(answers).index(answer)
            page_number = (answer_index // NUM_PER_PAGE) + 1
            url = reverse("question", args=[question_id])
            return redirect(f"{url}?page={page_number}#answer_{answer.id}")
        else:
            form.add_error(None, "Can't validate form")
    
    answers = Answer.objects.question_answers(question_id)
    return render(request, template_name="question.html",
                  context={"question" : question,
                           "answers" : pagination(request, answers, NUM_PER_PAGE),
                           "popular_tags": Tag.objects.popular_tags(20),
                           "form": form})
    