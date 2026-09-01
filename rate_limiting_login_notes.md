
# Rate limiting Django 

## Installer django-axes:
```bash 
pip install django-axes
pip freeze > requirements.txt
```

### Dans Settings.py

- Dans `INSTALLED_APPS` ajouter `axes`
- Dans `MIDDLEWARE` ajouter `axes.middleware.AxesMiddleware`
- Creer et completer `AUTHENTICATION_BACKEND`
- Faire la config a la fin 

```python 

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'axes',     # AJOUTER POUR AXE
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',   # AJOUTER CA POUR AXE
]

# AXE setups a faire ================================================================

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',   # doit etre en premier 
    'django.contrib.auth.backends.ModelBackend',
]

AXES_FAILURE_LIMIT = 5          # nombre d'echecs avant blocage
AXES_COOLOFF_TIME = 1           # duree du blocage, en heures
AXES_LOCKOUT_PARAMETERS = ['username', 'ip_address']   # bloque par email, pas juste par IP
```

#### Lancer les migrations :
```bash 
python3 manage.py makemigrations 
python3 manage.py migrate
```

## Deverouiller si besoin en dev

```bash
python3 manage.py axes_reset                            # reset tout 
python3 manage.py axes_reset_username kiki@gmail.com    # par identifiant
python3 manage.py axes_reset_ip 127.0.0.1               # par ip
```





