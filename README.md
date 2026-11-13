# form-django

## Install the packages requirements
```bash
pip install -r requirements.txt
```


## Launch Django development server
```bash
python manage.py runserver
```

## Create and apply changes in database
```bash
python manage.py migrate
```

## Change models and migrate in database to apply modification in the models
```bash
python manage.py makemigrations polls
python manage.py sqlmigrate polls 0001
```

## Check project conformity
```bash
python manage.py check
 ```

## Interactive Python shell to play with API
```bash
python manage.py shell
```

## Create an admin in database
```bash
python manage.py createsuperuser
```