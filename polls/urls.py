from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # /polls/all
    path("all/", views.AllPollsView.as_view(), name="all"),
    # /polls/statistics
    path("statistics/", views.statistics, name="statistics"),
    # ex: /polls/add
    path('add/', views.add, name='add'),
    # ex: /polls/confirm_add
    path('confirm_add/', views.confirm_add, name='confirm_add'),
    # ex: /polls/5/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # ex: /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    # ex: /polls/5/frequency/
    path("<int:pk>/frequency/", views.FrequencyView.as_view(), name="frequency"),
]
