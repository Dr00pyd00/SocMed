from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser


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
        self.client.login(**self.data)

        # Act 
        response = self.client.post(reverse('logout'))

        # Assert
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        

        
    def test_logout_required_post_not_get_fail(self):
        # Arrange
        # on utlise une methode test django qui bypass les view et login auto car on veut pas tester la logique de login ici
        self.client.login(**self.data)

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
        self.client.login(**self.data)

        # Act 
        self.client.post(reverse('logout'))
        response = self.client.get(reverse('home'))

        # Assert 
        self.assertFalse(response.wsgi_request.user.is_authenticated)



    





        

