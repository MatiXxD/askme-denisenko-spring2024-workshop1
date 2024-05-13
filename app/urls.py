from django.urls import path
from app import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hot/", views.hot, name="hot"),
    path("account_settings/", views.account_settings, name="account_settings"),
    path("list_by_tag/<tag>/", views.list_by_tag, name="list_by_tag"),
    path("login/", views.log_in, name="login"),
    path("new_question/", views.new_question, name="new_question"),
    path("question/<int:question_id>/", views.question, name="question"),
    path("registration/", views.registration, name="registration"),
    path("logout/", views.log_out, name="logout")
]
