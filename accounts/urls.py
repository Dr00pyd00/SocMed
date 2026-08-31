
from django.urls import path
from accounts import views

# pour reset le mdp
from django.contrib.auth import views as auth_views 

urlpatterns = [
        path('home/', views.home_view, name='home'),
        path('login/', views.login_view, name='login'),
        path('logout/', views.logout_view, name='logout'),
        path('register/', views.register_view, name='register'),

        # pour reset le mdp ==============================================================================================

        # Va demander l'email puis envoyer un mail a l'user avec le token dedans en GET:
        path(
            'password-reset/',
            auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
            name='password_reset'
            ),
        # Affiche juste une page pour dire : mail bien envoyer pour le reset
        path(
            'password-reset/done/',
            auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
            name='password_reset_done',
            ),
        # L'user arrive a cette view quand il click sur le lien recu:
        path(
            'reset/<uidb64>/<token>/',
            auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
            name='password_reset_confirm',
            ),
        # Page qui dit 'mdp changer avec success':
        path(
            'reset/done/',
            auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
            name='password_reset_complete',
            ),






    ]


