from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser

# pour tester un file ( image par exemple )
from django.core.files.uploadedfile import SimpleUploadedFile


# For register view ====================================================================================
class RegisterViewTest(TestCase):
    # Arrange
    good_data = {
                'email':'test@example.com',
                'password1':'GoodPassWord123',
                'password2':'GoodPassWord123',
                }

    
    def test_register_with_valid_data_create_user_success(self):
        # Act 
        response = self.client.post(reverse('register'), self.good_data)

        # Assert
        self.assertEqual(response.status_code, 302) # redirection apres formulaire 
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.first().email, 'test@example.com')


    def test_user_login_automatically_after_register_success(self):
        # Act 
        response = self.client.post(reverse('register'), self.good_data)

        # Assert 
        self.assertTrue(response.wsgi_request.user.is_authenticated)


    def test_register_with_mismateched_passwords_fail(self):
        # Arrange 
        bad_pw2_data = {**self.good_data, 'password2':'BadPassWord123'}

        # Act 
        response = self.client.post(reverse('register'), bad_pw2_data)

        # Assert
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertEqual(response.status_code, 200) # POURQUOI 200 ? car c'est l'http qui repond pas le prbleme server

    
    def test_register_with_existing_email_fail(self):
        # Arrange 
        CustomUser.objects.create_user(email=self.good_data['email'], password=self.good_data['password1'])

        # Act
        response = self.client.post(reverse('register'), self.good_data)

        # Assert
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_register_with_low_password_fail(self):
        # Arrange 
        bad_pw_data = {**self.good_data, 'password1':'123', 'password2':'123'}

        # Act 
        response = self.client.post(reverse('register'), bad_pw_data)

        # Assert
        self.assertEqual(CustomUser.objects.count(), 0)
                                  

# for login view =======================================================================================================
class  LoginViewTest(TestCase):
    data = {'email':'test@example.com','password':'GoodPassWord123'}
    def setUp(self) -> None:
        # Arrange
        # ATTENTION bien utiliser create_user !! sinon ca creer un object basic sans hacshage
        self.user = CustomUser.objects.create_user(**self.data)


    def test_login_with_good_credentials_redirect_success(self):
        # Act 
        response = self.client.post(reverse('login'), self.data)

        # Assert 
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.wsgi_request.user.is_authenticated, True)


    def test_login_with_bad_credential_pw_fail(self):
        # Act 
        response = self.client.post(reverse('login'), {**self.data, 'password':'BadPassWord123'})

        # Assert 
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 200)


    def test_login_with_inexistant_email_fail(self):
        # Act 
        response = self.client.post(reverse('login'), {**self.data, 'email':'bad@gmail.com'})

        # Assert 
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 200)

    
# logout tests ==================================================================================================
class LogoutViewTest(TestCase):
    data = {'email':'test@example.com','password':'GoodPassWord123'}

    def setUp(self) -> None:
        # Arrange
        self.user = CustomUser.objects.create_user(**self.data)

    def test_logout_sucess(self):
        # Arrange 
        self.client.force_login(self.user)

        # Act 
        response = self.client.post(reverse('logout'))

        # Assert
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        

        
    def test_logout_required_post_not_get_fail(self):
        # Arrange
        # on utlise une methode test django qui bypass les view et login auto car on veut pas tester la logique de login ici
        self.client.force_login(self.user)

        # Act 
        response = self.client.get(reverse('logout'))

        # Assert 
        self.assertEqual(response.status_code, 405)  # method not allowed

    def test_logout_when_not_login_fail(self):
        # Arrange 
        # on se login pas ...

        # Act 
        response = self.client.post(reverse('logout'))

        # Assert 
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, reverse('login')) #TODO marche pas met une url auto gerner plus complexe


    def test_logout_ends_session_sucess(self):
        # Arrange 
        self.client.force_login(self.user)

        # Act 
        self.client.post(reverse('logout'))
        response = self.client.get(reverse('home'))

        # Assert 
        self.assertFalse(response.wsgi_request.user.is_authenticated)



# profile tests =======================================================================================================

# Il faut un decorateur pour eviter de polluer physiquement le dossier Media:
import tempfile
from django.test import override_settings


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class ProfileViewTest(TestCase):

    data = {'email':'test@example.com','password':'GoodPassWord123'}

    def setUp(self):
        # Arrange
        self.user = CustomUser.objects.create_user(**self.data) # ici le signal va creer auto le profile

    def test_if_profile_exist_success(self):
        # Act 
        response = self.client.get(reverse('profile-view', args=[self.user.id]))

        # Assert 
        self.assertEqual(response.status_code, 200)


    def test_if_profile_not_exist_fail(self):
        # Act 
        response = self.client.get(reverse('profile-view', args=['999']))

        # Assert 
        self.assertEqual(response.status_code, 404)


    def test_profile_update_success(self):
        # Arrange
        self.client.force_login(self.user)
        new_data = {
            'pseudo': 'MonPseudo',
            'bio': 'Ma biographie',
            'website': 'https://example.com',
            'birth': '1990-05-15',
        }

        # Act 
        response = self.client.post(reverse('profile-edit'), new_data)
        self.user.profile.refresh_from_db() # ne pas oublier sinon update pas prise en compte en memoire

        # Assert 
        self.assertEqual(response.status_code, 302)     # car ya un redirect dans la view
        self.assertRedirects(response, reverse('profile-view', args=[self.user.pk])) # on cverifie la redirection precise
        self.assertEqual(self.user.profile.pseudo, new_data['pseudo'])
        self.assertEqual(self.user.profile.bio, new_data['bio'])



    def test_profile_update_fail(self):
        # Arrange
        self.client.force_login(self.user)
        new_data = {
            'pseudo': 'MonPseudo',
            'bio': 'Ma biographie',
            'website': 'BAD_MAIL',
            'birth': 'BAD_BIRTH',
        }

        # Act 
        response = self.client.post(reverse('profile-edit'), new_data)
        self.user.profile.refresh_from_db() # ne pas oublier sinon update pas prise en compte en memoire

        # Assert 
        self.assertEqual(response.status_code, 200)  # recharche le formulaire car ca fail
        self.assertNotEqual(self.user.profile.website, new_data['website'])
        self.assertNotEqual(self.user.profile.birth, new_data['birth'])


    def test_profile_update_without_login_fail(self):
        # Act 
        response = self.client.get(reverse('profile-edit'))

        # Assert 
        self.assertEqual(response.status_code, 302) # redirection vers LOGIN_URL


    def test_profile_update_with_avatar_success(self):
        # Arrange
        self.client.force_login(self.user)

        # une vraie image PNG minimale, en octets bruts
        image_content = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
            b'\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01'
            b'\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        avatar = SimpleUploadedFile('test.png', image_content, content_type='image/png')

        data = {
            'pseudo': 'MonPseudo',
            'bio': '',
            'website': '',
            'avatar': avatar,
        }

        # Act
        self.client.post(reverse('profile-edit'), data)
        self.user.profile.refresh_from_db()

        # Assert
        self.assertTrue(self.user.profile.avatar)
        self.assertIn('test', self.user.profile.avatar.name)


    def test_profile_update_with_avatar_fail(self):
        # Arrange 
        self.client.force_login(self.user)
        false_avatar = SimpleUploadedFile('bad_avatar.png', b'bad_image', content_type='image/png')

        data = {
            'pseudo': 'MonPseudo',
            'bio': '',
            'website': '',
            'avatar': false_avatar,
        }

        # Act 
        self.client.post(reverse('profile-edit'), data)
        self.user.profile.refresh_from_db()

        # Assert
        self.assertFalse(self.user.profile.avatar)
    





        

