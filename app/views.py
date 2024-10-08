import json
import time
import jwt

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.models import Question, Answer, Tag, Profile, QuestionLike, AnswerLike
from django.http import Http404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from app.forms import LoginForm, RegistrationForm, SettingsForm, QuestionForm, AnswerForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core.cache import cache
from cent import Client, PublishRequest
from django.contrib.postgres.search import SearchVector


def get_centrifugo_data(user_id):
    secret = settings.CENTRIFUGO_SECRET
    ws_url = settings.CENTRIFUGO_WS_URL
    token = jwt.encode(
        {"sub": str(user_id), "exp": int(time.time()) + 10*60}, secret, algorithm="HS256"
    )
    
    return {"centrifugo": {"token": token, "url": ws_url}}

def centrifugo_request(channel_name, username, text):
    api_key = settings.CENTRIFUGO_API_KEY
    api_url = settings.CENTRIFUGO_API_URL
    
    client = Client(api_url, api_key)
    request = PublishRequest(
        channel=channel_name, data={"username": username, "text": text}
    )
    
    client.publish(request)

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
    
def get_popular_tags(tags_count=20):
    popular_tags = cache.get("popular_tags")
    # if popular_tags is None:
    #     cache.set("popular_tags", Tag.objects.popular_tags(tags_count), 600)
    #     return cache.get("popular_tags")
    return popular_tags

def get_popular_members(member_count=5):
    popular_members = cache.get("popular_members")
    # if popular_members is None:
    #     cache.set("popular_members", Profile.objects.popular_profiles(member_count), 600)
    #     return cache.get("popular_members")
    return popular_members



def index(request):
    new_questions = Question.objects.new_questions()
    return render(request, template_name="index.html", 
                  context={"questions" : pagination(request, new_questions, 20),
                           "popular_tags": get_popular_tags(),
                           "popular_members": get_popular_members()})


def hot(request):
    hot_questions = Question.objects.hot_questions()
    return render(request, template_name="hot.html", 
                  context={"questions" : pagination(request, hot_questions, 20),
                           "popular_tags": get_popular_tags(),
                           "popular_members": get_popular_members()})

@csrf_protect
@login_required(redirect_field_name="continue")
def account_settings(request):
    user = request.user
    if request.method == "GET":
        form = SettingsForm()
    if request.method == "POST":
        form = SettingsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user)
            return render(request, template_name="account_settings.html",
                          context={"popular_tags": get_popular_tags(),
                                   "popular_members": get_popular_members(),
                                   "form": form, "saved": 1})
                      
    return render(request, template_name="account_settings.html",
                  context={"popular_tags": get_popular_tags(),
                           "popular_members": get_popular_members(),
                           "form": form, "saved": 0})


@csrf_protect
def log_in(request):
    if request.user.is_authenticated:
        return redirect(reverse("account_settings"))
    
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
        centrifugo_request
    return render(request, template_name="login.html",
                  context={"popular_tags": get_popular_tags(), 
                           "popular_members": get_popular_members(),
                           "login": login_form})


def log_out(request):
    logout(request)
    referer = request.META.get("HTTP_REFERER")
    return redirect(referer)

@csrf_protect
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
                  context={"popular_tags": get_popular_tags(),
                           "popular_members": get_popular_members(),
                           "form": user_form})


def list_by_tag(request, tag):
    try:
        questions_by_tag = Question.objects.questions_by_tag(tag)
    except Question.DoesNotExist:
        raise Http404
    return render(request, template_name="list_by_tag.html",
                  context={"questions" : pagination(request, questions_by_tag, 20),
                           "tag" : tag,
                           "popular_tags": get_popular_tags(),
                           "popular_members": get_popular_members()})


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
                  context={"popular_tags": get_popular_tags(),
                           "popular_members": get_popular_members(),
                           "form": form})


@csrf_protect
def question(request, question_id):
    NUM_PER_PAGE = 5
    channel_name = f"question_{question_id}"
    # channel_name = "test"
    
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
            centrifugo_request(channel_name, user.username, answer.text)
            return redirect(f"{url}?page={page_number}#answer_{answer.id}")
        else:
            form.add_error(None, "Can't validate form")
    
    answers = Answer.objects.question_answers(question_id)
    return render(request, template_name="question.html",
                  context={"question" : question,
                           "answers" : pagination(request, answers, NUM_PER_PAGE),
                           "popular_tags": get_popular_tags(),
                           "popular_members": get_popular_members(),
                           "form": form,
                           **get_centrifugo_data(request.user.id),
                           "channel_name" : channel_name})

@require_http_methods(["POST"])
@login_required()
@csrf_protect
def like_question(request, question_id):    
    body = json.loads(request.body)
    question = get_object_or_404(Question, id=question_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    question = Question.objects.liked_question(question, profile, body["pressedLike"])
        
    body["likes_count"] = question.likes_count
    body["dislikes_count"] = question.dislikes_count
        
    return JsonResponse(body)

@require_http_methods(["POST"])
@login_required()
@csrf_protect
def like_answer(request, answer_id):    
    body = json.loads(request.body)
    answer = get_object_or_404(Answer, id=answer_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    answer = Answer.objects.liked_answer(answer, profile, body["pressedLike"])
        
    body["likes_count"] = answer.likes_count
    body["dislikes_count"] = answer.dislikes_count
        
    return JsonResponse(body)


@require_http_methods(["POST"])
@login_required(redirect_field_name="continue")
@csrf_protect
def check_answer(request, question_id, answer_id):
    body = json.loads(request.body)
    question = get_object_or_404(Question, id=question_id)
    profile = get_object_or_404(Profile, user=request.user)
    answer = get_object_or_404(Answer, id=answer_id)

    if profile != question.author:
        body["isAuthor"] = False
    else:
        body["isAuthor"] = True
        answer.is_correct = not answer.is_correct
        print(answer.is_correct)
        answer.save()

    return JsonResponse(body)