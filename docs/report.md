## Initialiser un projet django

### Création d'un projet Django

```bash
django-admin startproject mysite djangotutorial
```
"djangotutotial" est un nom de dossier qui faut créer pour avoir le projet Django à l'intérieur.

### Création du dossier polls

```bash
python manage.py startapp polls
```

---

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

### Création d'utilisateurs

```pycon
from django.contrib.auth.models import User
user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
user.last_name = "Lennon"
user.save()
```

### Modification d'un mot de passe utilisateur

```pycon
from django.contrib.auth.models import User
user = User.objects.get(username="john")
u.set_password("new password")
user.save()
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

### Example Admin model

```pycon
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["question_text"]
    ordering = ["pub_date"]
    search_fields = ["question_text"]
```

On peut ajouter dans le tableau de la variable liste_display les méthodes du modèle.

### Different method to display in application

Pour avoir comme un modèle admin "Choice" et de voir toute sa liste.

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

---

### Savoir où sont les fichiers source de Django

```shell
python -c "import django; print(django.__path__)"
```

---

## Gestion des données des utilisateurs

### Création d'un superutilisateur

```shell
python manage.py createsuperuser --username=joe --email=joe@example.com
```

Créer ensuite votre mot de passe.

On peut le créer sans argument et qu'il faudra saisir par la suite de cette commande:

```shell
python manage.py createsuperuser
```

### Modification d'un mot de passe d'un utilisateur

```shell
django-admin changepassword <superuser>
```

### Authentification d'un utilisateur

```python
from django.contrib.auth import authenticate

user = authenticate(username="john", password="secret")
if user is not None:
    # A backend authenticated the credentials
    ...
else:
    # No backend authenticated the credentials
    ...
```

### Création de permission

```python
from myapp.models import BlogPost
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_model(BlogPost)
permission = Permission.objects.create(
    codename="can_publish",
    name="Can Publish Posts",
    content_type=content_type,
)
```

## Requête d'authentification Web

### Vérification d'authentification de l'utilisateur

En synchrone:

```python
if request.user.is_authenticated:
    # Do something for authenticated users.
    ...
else:
    # Do something for anonymous users.
    ...
```

En asynchrone:

```python
user = await request.auser()
if user.is_authenticated:
    # Do something for authenticated users.
    ...
else:
    # Do something for anonymous users.
    ...
```

### Exemple de code en Python pour authentification

```python
from django.contrib.auth import authenticate, login


def my_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...
```

### Déconnexion de l'utilisateur

```python
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    # Redirect to a success page.
```

Possibilité de la faire en asynchrone avec la méthode `alogout(request)`.

### Rediriger vers la page de connexion si pas authentifier

```python
from django.conf import settings
from django.shortcuts import redirect


@login_required(redirect_field_name="my_redirect_field", login_url="/accounts/login/")
def my_view(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    # ...
```

### Afficher un message d'erreur pour non authentification

```python
from django.shortcuts import render


@login_required
def my_view(request):
    if not request.user.is_authenticated:
        return render(request, "myapp/login_error.html")
    # ...
```

Si aucune page de connexion n'est paramétré, il faudra créer une vue d'authentification.

```python
from django.contrib.auth import views as auth_views

path("accounts/login/", auth_views.LoginView.as_view()),
```

### Rendu pour réussite de connexion ou de la création d'un utilisateur

```HTML
{% if user.is_authenticated %}
<p>Welcome, {{ user.username }}. Thanks for logging in.</p>
{% else %}
<p>Welcome, new user. Please log in.</p>
{% endif %}
```

### Vérification de la permission dans le gabarit

```HTML
{% if perms.foo %}
<p>You have permission to do something in the foo app.</p>
{% if perms.foo.add_vote %}
<p>You can vote!</p>
{% endif %}
{% if perms.foo.add_driving %}
<p>You can drive!</p>
{% endif %}
{% else %}
<p>You don't have permission to do anything in the foo app.</p>
{% endif %}
```

```HTML
{% if 'foo' in perms %}
{% if 'foo.add_vote' in perms %}
<p>In lookup works, too.</p>
{% endif %}
{% endif %}
```

