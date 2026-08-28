
from django import forms

class LoginForm(forms.Form):
    """ 
    2 mecanisms:
    - validate data in view ( style pydantic )
    - create html form auto {{form.as_p}}
    """
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

