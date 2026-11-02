# form-django

## Launch Django development server
```
python manage.py runserver
```

## Create and apply changes in database
```
python manage.py migrate
```

## Change models and migrate in database to apply modification in the models
```
python manage.py makemigrations polls
```
```
python manage.py sqlmigrate polls 0001
```

## Check project conformity
```
python manage.py check
 ```

## Interactive Python shell to play with API
```
python manage.py shell
```

## Create an admin in database
```
python manage.py createsuperuser
```