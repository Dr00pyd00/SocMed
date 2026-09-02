
from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import CustomUser, UserProfile

# Login ===================================================================
class LoginForm(forms.Form):
    """ 
    2 mecanisms:
    - validate data in view ( style pydantic )
    - create html form auto {{form.as_p}}
    """
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

# Register ================================================================
class RegisterForm(UserCreationForm):
    """
    Formulaire for create a new account
    """
    # on ajoute le champ et le rend obligatoire
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        # precise le champ voulu, ici par username 
        fields = ['email']

# Edit Profile =============================================================
class EditProfileForm(forms.ModelForm):
    """
    Form for edit the UserProfile.
    - birth force to be type date 
    """
    class Meta:
        model = UserProfile
        fields = ['pseudo','birth','bio','avatar','website']
        # ici widgert sert a forcer l'html avec <input type="date" name="birth">
        # au lieu de <input type="text" name="birth"> 
        widgets = {
                'birth': forms.DateInput(attrs={'type':'date'}),
                }



