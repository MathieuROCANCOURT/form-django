import this
from builtins import sum

from django.db.models import F, Sum, Max
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views import generic

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class AllPollsView(generic.ListView):
    template_name = "polls/all_polls.html"
    context_object_name = "question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")


class StatisticsView(generic.ListView):
    template_name = "polls/statistics.html"
    context_object_name = "all_statistics"

    def get_queryset(self):
        nb_questions = Question.objects.count()
        nb_choices = Choice.objects.count()
        nb_total_votes = Choice.objects.aggregate(total_votes=Sum("votes")).get("total_votes")
        last_question = Question.objects.aggregate(recent_question=Max("pub_date")).get("recent_question")

        return nb_questions, nb_choices, nb_total_votes, 0 if nb_questions == 0 else nb_total_votes / nb_questions, last_question


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


class FrequencyView(generic.DetailView):
    model = Question
    template_name = "polls/frequency.html"


@require_http_methods(["POST"])
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
