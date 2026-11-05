import datetime

from django.db import models
from django.utils import timezone
from django.db.models import Sum

MAX_LENGTH = 20


def text_excerpt(text, max_length):
    return text[:max_length] + ('...' if len(text) > max_length else '')


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return "{} {}".format(self.pub_date, text_excerpt(self.question_text, MAX_LENGTH))

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def age(self):
        return timezone.now() - self.pub_date

    def get_choices(self):
        choices = self.choice_set.all()
        resultat = self.choice_set.aggregate(total=Sum('votes'))
        total = resultat['total'] or 0
        result = []
        for choice in choices:
            percentage = None
            if total != 0:
                percentage = 100 * choice.votes / total
            result.append((choice.choice_text, choice.votes, percentage))
        return result

    def get_max_choice(self):
        choices = self.choice_set.all()
        resultat = self.choice_set.aggregate(total=Sum('votes'))
        total = resultat['total'] or 0
        max_choice = max(choices, key=lambda c: c.votes / total)
        return max_choice.choice_text, max_choice.votes / total if total > 0 else None


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return text_excerpt(self.choice_text, MAX_LENGTH)
