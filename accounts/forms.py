
from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import CustomUser

class LoginForm(forms.Form):
    """ 
    2 mecanisms:
    - validate data in view ( style pydantic )
    - create html form auto {{form.as_p}}
    """
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    """

    """
    # on ajoute le champ et le rend obligatoire
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        # precise le champ voulu, ici par username 
        fields = ['email']

