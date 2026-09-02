from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse

from accounts.forms import EditProfileForm, LoginForm, RegisterForm
from accounts.models import CustomUser


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
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                # c'est le @required_login qui inject le ?next auto on le recup ici si il existe, dans le html il faut le catch et le donner ici grace a un input hidden
                next_url = request.POST.get('next') or request.GET.get('next') or 'home'
                return redirect(next_url)
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
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form':form})



@login_required
def edit_profile_view(request):
    # on chope le profile du current user pour modifier cette instance 
    profile = request.user.profile
    if request.method == 'POST':
        # on doit mettre request.FILES car c'est par cette objet que l'image transit
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile-view', pk=request.user.pk)
    else:
        form = EditProfileForm(instance=profile)

    return render(request, 'accounts/profile_edit.html', {'form':form})


def profile_view(request, pk):
    profile_user = get_object_or_404(CustomUser, pk=pk)
    profile = profile_user.profile
    return render(request, 'accounts/profile_view.html', {'profile':profile, 'profile_user':profile_user})






