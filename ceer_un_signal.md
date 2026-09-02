
# Un signal Django

Un signal Django est un mécanisme qui permet d'exécuter automatiquement du code à chaque fois qu'un événement précis se produit.

Par exemple: creer un profile des que un User est creer , pas en passant par `views.py` car ca marcherai pas pour objects.create_user().



## Creer le signal:

Dans accounts/signals.py:

```python 
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

- `@receiver` = decorateur qui sert a connecter cette fonction a un evenement
- `post_save` = type d'evement, ici : **"juste apres qu'un objet soit save en db"**
- `sender` = cible un objet en particulier
- `created` = un booléen que Django fournit automatiquement : True si l'objet vient d'être créé pour la première fois, False si c'était juste une mise à jour d'un objet existant.
        


## Il faut enregistrer le signal dans apps

```python 
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals
```

- `def ready()` : method special apeler au demarrage de l'app , ducoup on prend en compte les signals a ce moment.



