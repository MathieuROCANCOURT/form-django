from django.db.models import F, Sum, Max
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views import generic

from .utils import minimax
from .models import Question, Choice
from .forms import NameForm

NB_MAX_CHOIX = 5


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


@require_http_methods(["GET"])
def add(request):
    return render(request, 'polls/add.html', {
        'liste_no_choix': range(NB_MAX_CHOIX)
    })


@require_http_methods(["POST"])
def confirm_add(request):
    # récupération du libellé de la question,
    # sans les éventuels espaces avant et après
    question_text = request.POST['question_text'].strip()
    if question_text:
        # ajout de la question si elle n'est pas vide
        question = Question(question_text=question_text,
                            pub_date=timezone.now())
        question.save()

        # on traite à présent les champs de choix remplis
        # (on s'arrête au premier vide)
        for no_choix in range(NB_MAX_CHOIX):
            nom_champ = 'choix_{}'.format(no_choix)
            choice_text = request.POST[nom_champ].strip()
            if choice_text:
                choice = Choice(question=question,
                                choice_text=choice_text)
                choice.save()
            else:
                break
        return render(request, 'polls/confirm_add.html')
    else:
        # réaffichage du formulaire de saisie de la question
        # avec le message d'erreur
        return render(request, 'polls/add.html', {
            'error_message': "You didn't enter a question text",
        })


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


class FrequencyView(generic.DetailView):
    model = Question
    template_name = "polls/frequency.html"


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, "name.html", {"form": form})


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
