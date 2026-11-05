Lors des créations des nouvelles interfaces et en ajoutant les 5 questions où chaque question a 3 choix, on peut voir
tous les attributs de mes classes "Questions" et "Choices" en voyant les attributs sans les identifiants.
Aucune filtration, triage ou de recherche d'un contenu ne peut être fait.
---
Pour modifier l'accès d'un utilisateur vers une vue de super-user, cocher les cases "Status équipe" et "Status
super-utilisateur" dans la section "Permissions".

Pour rendre inactif le compte, dans la section "Permissions", décochez la case "Actif".

<b style="color: red">Sauvegarder pour chaque modification.</b>

---

## Shell Django

### Affichage de tous les attributs de chaque question

```pycon
[(question.question_text, question.pub_date) for question in Question.objects.all()]
```

### Filtrage en fonction d'une date.

```pycon
import datetime as dt
[(question.question_text, question.pub_date) for question in Question.objects.all() if question.pub_date.date() <= dt.date(2010,12,4)]
```

### Récupérer tous les attributs de l'objet "Choix" où la question a pour id qui vaut 2.

```pycon
[(choice.question.question_text, choice.question.pub_date, choice.choice_text, choice.votes) for choice in Choice.objects.all() if choice.question.id == 2]
```

### Récupérer pour chaque question, tous les choix avec toutes les attributs.

```pycon
for question in Question.objects.all():
     print(question.question_text, question.pub_date)
     for choice in Choice.objects.filter(question__id=question.id):
             print(choice.choice_text, choice.votes)
```

```pycon
for question in Question.objects.all():
     print(question.question_text, question.pub_date)
     print(Choice.objects.filter(question__id=question.id))
```

### Afficher le nombre de choix pour chaque question.

```pycon
for question in Question.objects.all():
     print(question.question_text, question.pub_date)
     print("Nombre de choix:", len(Choice.objects.filter(question__id=question.id)))
```

### Trier les questions par ordre antéchronologique.

```pycon
Question.objects.all().order_by("pub_date").reverse()
```

### Création d'une question en utilisant le shell.

```pycon
import datetime as dt
q = Question(question_text="Es-tu là ?", pub_date=dt.datetime.now())
q.save()
```

---

## View file

### Import F, Sum and Max and application

Dans le fichier view.py, on peut faire des applications d'agrégations pour la somme, le minimum, le maximum, la
moyenne, … (https://docs.djangoproject.com/fr/5.2/topics/db/aggregation/).

```pycon
from django.db.models import F, Sum, Max

#...
Question.objects.aggregate(recent_question=Max("pub_date")).get("recent_question")
#...
```

En cas de non d'affection dans l'argument aggregate, {valeur du String}__sum.

## Admin file

### Different method to display in application

Pour avoir comme un modèle admin "Choice" et de voir tout sa liste. 
```pycon
class Choice(admin.ModelAdmin): ...
```

Voir le modèle bloc par bloc les choix dans la question avec un ajout de 3 blocs par défaut.
```pycon
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3
```

Voir le modèle comme un tableau les choix dans la question.
```pycon
class ChoiceInline(admin.TabularInline): ...
```