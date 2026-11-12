from django.db.models import F, Sum, Max
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views import generic
from django.contrib.auth.decorators import login_required

from .utils import minimax
from .models import Question, Choice
from .forms import QuestionAddForm

PATH_DETAIL_HTML = "polls/detail.html"
NB_MAX_CHOICES = 5


@require_http_methods(["GET"])
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


class AllPollsView(generic.ListView):
    template_name = "polls/all_polls.html"
    context_object_name = "question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")


@require_http_methods(["GET"])
def statistics(request):
    nb_questions = Question.objects.count()
    nb_choices = Choice.objects.count()
    nb_total_votes = Choice.objects.aggregate(total_votes=Sum("votes")).get("total_votes")
    average_by_poll = 0 if nb_questions == 0 else nb_total_votes / nb_questions
    least_popular_question, most_popular_question = minimax()
    id_last_question = Question.objects.aggregate(max=Max('id'))['max']

    return render(request, 'polls/statistics.html', {
        'nb_questions': nb_questions,
        'nb_choices': nb_choices,
        'nb_total_votes': nb_total_votes,
        'average_by_poll': average_by_poll,
        'most_popular_question': most_popular_question,
        'least_popular_question': least_popular_question,
        'last_question': id_last_question,
    })


@login_required(login_url="polls:login")
@require_http_methods(["GET"])
def confirm_add(request):
    return render(request, 'polls/confirm_add.html', {
        'liste_no_choix': range(NB_MAX_CHOICES)
    })


@login_required(login_url="polls:login")
def add(request):
    if request.method == 'POST':
        form = QuestionAddForm(request.POST)
        if form.is_valid():
            question = Question(question_text=form.cleaned_data['question_text'],
                                pub_date=timezone.now())
            question.save()
            # on traite à présent les champs de choix remplis
            # (on s'arrête au premier vide)
            for no_choix in range(NB_MAX_CHOICES):
                nom_champ = 'choice_{}'.format(no_choix)
                choice_text = form.cleaned_data[nom_champ].strip()
                if choice_text:
                    choice = Choice(question=question,
                                    choice_text=choice_text)
                    choice.save()
                else:
                    break
            return redirect('polls:confirm_add')
    else:
        form = QuestionAddForm()
    return render(request, 'polls/add.html', {'form': form})


class DetailView(generic.DetailView):
    model = Question
    template_name = PATH_DETAIL_HTML


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


class FrequencyView(generic.DetailView):
    model = Question
    template_name = "polls/frequency.html"


@require_http_methods(["GET"])
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, PATH_DETAIL_HTML, {"question": question})


@require_http_methods(["POST"])
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            PATH_DETAIL_HTML,
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
