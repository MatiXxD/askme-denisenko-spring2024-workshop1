from django.shortcuts import render
from django.core.paginator import Paginator


QUESTIONS = [
    {
        "id" : i,
        "title": f"Question {i}",
        "text": f"Some text for question {i}"
    } for i in range(1, 100)
]

HOT_QUESTIONS = [
    {
        "id" : i,
        "title": f"Question {i}",
        "text": f"Some text for question {i}"
    } for i in range(99, 1, -1)
]

QUESTIONS_BY_TAG = [
    {
        "id" : i,
        "title": f"Question {i}",
        "text": f"Some text for question {i}"
    } for i in range(1, 100, 5)
]


ANSWERS = [ 
    [f"Answer number {j} for question {i}" for j in range(1, 20)] 
for i in range(1, 100)]



def __get_page_obj(request, questions, per_page):
    page_num = request.GET.get("page", 1)
    paginator = Paginator(questions, per_page=per_page)
    return paginator.page(page_num)
    



def index(request):
    return render(request, template_name="index.html", 
                  context={"questions" : __get_page_obj(request, QUESTIONS, 20)})

def hot(request):
    return render(request, template_name="hot.html", 
                  context={"questions" : __get_page_obj(request, HOT_QUESTIONS, 20)})

def account_settings(request):
    return render(request, template_name="account_settings.html",
                  context={"nickname" : "some_nickname"})

def login(request):
    return render(request, template_name="login.html")

def registration(request):
    return render(request, template_name="registration.html")

def list_by_tag(request, tag):
    return render(request, template_name="list_by_tag.html",
                  context={"questions" : __get_page_obj(request, QUESTIONS_BY_TAG, 20),
                           "tag" : tag})

def new_question(request):
    return render(request, template_name="new_question.html")

def question(request, question_id):
    return render(request, template_name="question.html",
                  context={"question" : QUESTIONS[question_id-1],
                           "answers" : __get_page_obj(request, ANSWERS[question_id-1], 5)})
