from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from posts.models import Post

User = get_user_model()


# BASE
class PostBaseTest(TestCase):
    """ basics arranges for tests about posts """
    def setUp(self):
        self.owner = User.objects.create_user(
                email='owner@example.com',
                password='GoodPassword123',
                )
        self.other = User.objects.create_user(
                email='other@example.com',
                password='GoodPassword123',
                )
        self.post = Post.objects.create(
                user=self.owner,
                text='test post',
                )
        

# Creations posts ============================================================================================
# CAREFUL: setup already create a post from orm: donc creer un post via les vues et checker ce post en particulier 
class PostCreateTest(PostBaseTest):

    def test_authenticated_user_create_post_success(self):
        # Arrange
        self.client.force_login(self.owner)
        post_data = {'text':'test data post'}
        # Act 
        response = self.client.post(reverse('posts:post-creation'), post_data)
        # Assert 
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
                Post.objects.filter(text='test data post').exists()
                )
        created_post = Post.objects.get(text='test data post')
        self.assertEqual(created_post.user, self.owner)

    def test_not_authenticated_user_create_post_fail(self):
        # Arrange
        post_data = {'text':'test data post'}
        # Act 
        response = self.client.post(reverse('posts:post-creation'), post_data)
        # Assert
        self.assertEqual(response.status_code, 302) # redirction car @login_required for un rediret (parfois avec next)
        self.assertFalse(Post.objects.filter(text='test data post').exists())


class PostDetailTest(PostBaseTest):

    def test_detail_view_authenticated_user_success(self):
        # Arrange 
        self.client.force_login(self.owner)
        # Act 
        response = self.client.get(reverse('posts:post-detail', kwargs={'pk': self.post.id}))
        # Assert 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.text)

    def test_detail_view_not_authenticated_user_success(self):
        # Arrange 
            # on login pas.
        # Act 
        response = self.client.get(reverse('posts:post-detail', kwargs={'pk': self.post.id}))
        # Assert 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.text)

    def test_detail_view_inexistant_post(self):
        # Act 
        response = self.client.get(reverse('posts:post-detail', kwargs={'pk':99999}))
        # Assert
        self.assertEqual(response.status_code, 404)


class PostUpdateTest(PostBaseTest):

    new_data = {
                'text':'updated text',
                }

    def test_update_post_with_owner_success(self):
        # Arrange
        self.client.force_login(self.owner)
        # Act
        response = self.client.post(reverse('posts:post-update', kwargs={'pk':self.post.id}), self.new_data)
        # Assert
        self.assertRedirects(response, reverse('posts:post-detail',kwargs={'pk':self.post.id}), status_code=302)  #TODO  302 car de base cest une redirection ? bizarre.
        updated_post = Post.objects.get(pk=self.post.id)
        self.assertEqual(updated_post.text, self.new_data['text'])

    def test_update_post_with_user_not_owner_fail(self):
        # Arrange
        self.client.force_login(self.other)
        # Act
        response = self.client.post(reverse('posts:post-update',kwargs={'pk':self.post.id}), self.new_data)
        # Assert 
        self.assertEqual(response.status_code, 403)
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.text, self.new_data['text'])

    def test_update_post_with_anonymous_user_fail(self):
        # Act 
        response = self.client.post(reverse('posts:post-update',kwargs={'pk':self.post.id}), self.new_data)
        # Assert 
        self.assertEqual(response.status_code, 302) # vers login 
        self.assertIn(reverse('accounts:login'), response.url)

    def test_update_inexistant_post_fail(self):
        # Arrange
        self.client.force_login(self.owner)
        # Act 
        response = self.client.post(reverse('posts:post-update',kwargs={'pk':9999}), self.new_data)
        # Assert 
        self.assertEqual(response.status_code, 404)



    


        
         


