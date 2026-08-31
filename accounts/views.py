from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse

from accounts.forms import LoginForm, RegisterForm


# Create your views here.

def home_view(request):
    return render(request, 'accounts/index.html')


def login_view(request):
    """ 
    Function view for the login 
    - if login work : go to homepage
    - if empty fields : reset the login page
    - if bad cred : reset the login page with error message setup
    - if not POST method : return form login page too
    """
    if request.method == 'POST':
        # on prend les donnees de la page html puis on les donne au forms pour quil teste
        # et on regarde si c'est valide 
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # ici logique de connexion return None si les cred ne correspondent pas 
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # vu que User est not None l'auth a reussi , plus besoin de pw
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Incorrect Credentials')
    else:
        form = LoginForm() # formulaire vide pour affichage initial 

    return render(request, 'accounts/login.html', {'form':form} )


# le login_required envoi vers LOGIN_URL et rajoute ?next='la on on etait avant de cliquer' comme ca ca redirige
# exemple je me connecte a /profile  mais pas login:
#   ca envoir vers LOGIN_URL?next=/profile 
#   et une fois login ca lis le next automatiquement aller sur l'url ?
@login_required # si non login ca prend l'url LOGIN_URL dans settings ( accounts/login/ par defaut ) 
@require_POST
def logout_view(request):
    """ 
    Function view for login.
    - login_required : if not login redirect to LOGIN_URL
    - require_POST : only work when the method is POST
    """
    logout(request)
    return redirect('home')
    

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form':form})









