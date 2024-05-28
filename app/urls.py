from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("hot/", views.hot, name="hot"),
    path("account_settings/", views.account_settings, name="account_settings"),
    path("list_by_tag/<tag>/", views.list_by_tag, name="list_by_tag"),
    path("login/", views.log_in, name="login"),
    path("new_question/", views.new_question, name="new_question"),
    path("question/<int:question_id>/", views.question, name="question"),
    path("registration/", views.registration, name="registration"),
    path("logout/", views.log_out, name="logout"),
    path("<int:question_id>/like_question", views.like_question, name="like_question"),
    path("<int:answer_id>/like_answer", views.like_answer, name="like_answer"),
    path("<int:question_id>/<int:answer_id>/check_answer", views.check_answer, name="check_answer"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)