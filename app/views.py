from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.models import Question, Answer, Tag



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

def account_settings(request):
    return render(request, template_name="account_settings.html",
                  context={"nickname" : "some_nickname",
                           "popular_tags": Tag.objects.popular_tags(20)})

def login(request):
    return render(request, template_name="login.html",
                  context={"popular_tags": Tag.objects.popular_tags(20)})

def registration(request):
    return render(request, template_name="registration.html",
                  context={"popular_tags": Tag.objects.popular_tags(20)})

def list_by_tag(request, tag):
    questions_by_tag = Question.objects.questions_by_tag(tag)
    return render(request, template_name="list_by_tag.html",
                  context={"questions" : pagination(request, questions_by_tag, 20),
                           "tag" : tag,
                           "popular_tags": Tag.objects.popular_tags(20)})

def new_question(request):
    return render(request, template_name="new_question.html",
                  context={"popular_tags": Tag.objects.popular_tags(20)})

def question(request, question_id):
    question = Question.objects.question_by_id(question_id)
    answers = Answer.objects.question_answers(question_id)
    return render(request, template_name="question.html",
                  context={"question" : question,
                           "answers" : pagination(request, answers, 5),
                           "popular_tags": Tag.objects.popular_tags(20)})
