from django.db.models import Sum
from .models import Question, Choice


def minimax():
    questions = Question.objects.all()
    _min = _max = (questions[0], 0)
    for q in questions:
        n = q.choice_set.aggregate(sum=Sum('votes'))['sum']
        if n is not None and n > _max[1]:
            _max = (q, n)
        if n is not None and n < _min[1]:
            _min = (q, n)
    return _min[0], _max[0]
