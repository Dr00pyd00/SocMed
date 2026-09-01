from django.conf import settings
from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager


# =============== USER setup  ========================================================
class CustomUserManager(BaseUserManager):
    """
    tool for manager the CustomUsers creations etc 
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email required!')
        # clean mail
        email = self.normalize_email(email)
        # self model => lien avec le CustomUser 
        user = self.model(email=email, **extra_fields)
        # set password 
        user.set_password(password)
        # adaptation de la db 
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser need : is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser need : is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    custom user: EMAIL as principal credential ( not username ) 
    """
    # retire le username 
    username = None 
    # force uniaue mail
    email = models.EmailField(unique=True)
    # mettre mail en defaut de cred 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # simple pour createsuperuser
    # branche le manager 
    objects = CustomUserManager()

    def __str__(self):
        return self.email


# ========================== Profile ======================================
class UserProfile(models.Model):
    """ 
    All data of a User to display a Profile Page for example 
    """ 
    # TODO mettre en place avatars avec dossier images et tout 

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    pseudo = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.email 



