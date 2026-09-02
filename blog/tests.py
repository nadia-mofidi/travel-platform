from django.test import TestCase
from blog.models import Post,Category,Comment
from django.contrib.auth.models import User,Group
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
# Create your tests here.

class PostModelTest(TestCase):
    def test_post_creation(self):
        post = Post.objects.create(
            title = 'Django Test',
            content = 'Testing django.'
        )
        self.assertEqual(post.title,'Django Test')
        self.assertEqual(post.content, 'Testing django.')
    
    def test_post_default_values(self):
        post = Post.objects.create(
            title = 'title test',
            content = 'content test.'
        )
        self.assertEqual(post.counted_views,0)
        self.assertFalse(post.status)
        self.assertFalse(post.is_featured)
        self.assertFalse(post.login_require)

    def test_post_get_absolute_url(self):
        post = Post.objects.create(
            title='title test',
            content='content test.'
        )

        self.assertEqual(post.get_absolute_url(),
            reverse('blog:single', kwargs={'pid': post.id})
        )
    
    def test_post_user_connection(self):
        user = User.objects.create_user(
        username='testuser',
        password='testpass123'
        )
        post = Post.objects.create(
            title='title test',
            content='content test.',
            author=user
        )
        self.assertEqual(post.author,user)

class BlogViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testauthor',
            password='testpass123'
        )

    def test_blog_view(self):
        response = self.client.get(
            reverse('blog:index')
        )

        self.assertEqual(response.status_code, 200)
    
    def test_blog_view_only_shows_published_posts(self):
        
        published_post = Post.objects.create(
            title='Published Post',
            content='Published content.',
            author=self.user,
            status=True,
            publish_date=timezone.now() - timedelta(days=1)
        )

        draft_post = Post.objects.create(
            title='Draft Post',
            content='Draft content.',
            author=self.user,
            status=False,
            publish_date=timezone.now() - timedelta(days=1)
        )

        response = self.client.get(reverse('blog:index'))

        self.assertContains(response, published_post.title)
        self.assertNotContains(response, draft_post.title)

    def test_blog_view_does_not_show_future_posts(self):
        future_post = Post.objects.create(
            title='Future Post',
            content='Future content.',
            author=self.user,
            status=True,
            publish_date=timezone.now() + timedelta(days=1)
        )

        response = self.client.get(reverse('blog:index'))

        self.assertNotContains(response, future_post.title)

    def test_blog_category_filter(self):
        category1 = Category.objects.create(name='Technology')
        category2 = Category.objects.create(name='Travel')

        post1 = Post.objects.create(
            title='Django Post',
            content='Django content.',
            author=self.user,
            status=True,
            publish_date=timezone.now() - timedelta(days=1)
        )

        post2 = Post.objects.create(
            title='Travel Post',
            content='Travel content.',
            author=self.user,
            status=True,
            publish_date=timezone.now() - timedelta(days=1)
        )

        post1.category.add(category1)
        post2.category.add(category2)

        response = self.client.get(
            reverse('blog:category', kwargs={'cat_name': 'Technology'})
        )

        self.assertContains(response, post1.title)
        self.assertNotContains(response, post2.title)

    def test_blog_author_filter(self):
        another_user = User.objects.create_user(
            username='anotherauthor',
            password='testpass123'
        )

        post1 = Post.objects.create(
            title='My Post',
            content='My content.',
            author=self.user,
            status=True,
            publish_date=timezone.now() - timedelta(days=1)
        )

        post2 = Post.objects.create(
            title='Another Author Post',
            content='Another content.',
            author=another_user,
            status=True,
            publish_date=timezone.now() - timedelta(days=1)
        )

        response = self.client.get(
            reverse(
                'blog:author',
                kwargs={'auth_username': self.user.username}
            )
        )

        self.assertContains(response, post1.title)
        self.assertNotContains(response, post2.title)

    def test_blog_tag_filter(self):
        post1 = Post.objects.create(
            title='Tagged Post',
            content='Tagged content.',
            author=self.user,
            status=True,
            publish_date=timezone.now() - timedelta(days=1)
        )

        post2 = Post.objects.create(
            title='Untagged Post',
            content='Untagged content.',
            author=self.user,
            status=True,
            publish_date=timezone.now() - timedelta(days=1)
        )

        post1.tags.add('test')

        response = self.client.get(
            reverse(
                'blog:tags',
                kwargs={'tag_name': 'test'}
            )
        )

        self.assertContains(response, post1.title)
        self.assertNotContains(response, post2.title)

    def test_blog_search(self):
        matching_post = Post.objects.create(
            title='Django Tutorial',
            content='Learn Django.',
            author=self.user,
            status=True,
            publish_date=timezone.now() - timedelta(days=1)
        )

        other_post = Post.objects.create(
            title='Travel Guide',
            content='A guide about traveling.',
            author=self.user,
            status=True,
            publish_date=timezone.now() - timedelta(days=1)
        )

        response = self.client.get(
            reverse('blog:search'),
            {'s': 'Django'}
        )

        self.assertContains(response, matching_post.title)
        self.assertNotContains(response, other_post.title)
    
    def test_login_required_post_redirects_anonymous_user(self):
        post = Post.objects.create(
            title='Private Post',
            content='Private content.',
            author=self.user,
            status=True,
            login_require=True,
            publish_date=timezone.now() - timedelta(days=1)
        )

        response = self.client.get(
            reverse('blog:single', kwargs={'pid': post.id})
        )

        self.assertRedirects(
            response,
            reverse('accounts:login')
        )

    def test_authenticated_user_can_view_private_post(self):
        post = Post.objects.create(
            title='Private Post',
            content='Private content.',
            author=self.user,
            status=True,
            login_require=True,
            publish_date=timezone.now() - timedelta(days=1)
        )

        self.client.login(
            username='testauthor',
            password='testpass123'
        )

        response = self.client.get(
            reverse('blog:single', kwargs={'pid': post.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)

    def test_blog_single_returns_404_for_invalid_post(self):
        response = self.client.get(
            reverse('blog:single', kwargs={'pid': 99999})
        )

        self.assertEqual(response.status_code, 404)

    def test_blog_single_shows_only_approved_comments(self):
        post = Post.objects.create(
            title='Comment Test Post',
            content='Post content.',
            author=self.user,
            status=True,
            publish_date=timezone.now() - timedelta(days=1)
        )

        approved_comment = Comment.objects.create(
            post=post,
            name='Approved User',
            email='approved@test.com',
            subject='Approved',
            message='This comment is approved.',
            approved=True
        )

        pending_comment = Comment.objects.create(
            post=post,
            name='Pending User',
            email='pending@test.com',
            subject='Pending',
            message='This comment is waiting.',
            approved=False
        )

        response = self.client.get(
            reverse('blog:single', kwargs={'pid': post.id})
        )

        self.assertContains(response, approved_comment.message)
        self.assertNotContains(response, pending_comment.message)

    def test_comment_submission(self):
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            status=True,
            publish_date=timezone.now()
        )

        response = self.client.post(
            reverse('blog:single', kwargs={'pid': post.id}),
            {
                'name': 'Test User',
                'email': 'test@example.com',
                'subject': 'Test Subject',
                'message': 'This is a test comment.'
            }
        )

        self.assertRedirects(
            response,
            reverse('blog:single', kwargs={'pid': post.id})
        )

        self.assertTrue(
            Comment.objects.filter(
                post=post,
                message='This is a test comment.'
            ).exists()
        )

    def test_comment_requires_message(self):
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            status=True,
            publish_date=timezone.now()
        )

        response = self.client.post(
            reverse('blog:single', kwargs={'pid': post.id}),
            {
                'name': 'Test User',
                'email': 'test@example.com',
                'subject': 'Test Subject',
                'message': ''
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Comment.objects.filter(post=post).exists()
        )

class AuthenticationTest(TestCase):

    def test_signup(self):
        response = self.client.post(
            reverse('accounts:signup'),
            {
                'username': 'newuser',
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'test@example.com',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            }
        )

        self.assertRedirects(
            response,
            reverse('accounts:login')
        )

        self.assertTrue(
            User.objects.filter(username='newuser').exists()
        )

    def test_login(self):
        User.objects.create_user(
            username='loginuser',
            password='StrongPass123!'
        )

        response = self.client.post(
            reverse('accounts:login'),
            {
                'username': 'loginuser',
                'password': 'StrongPass123!'
            }
        )

        self.assertRedirects(
            response,
            reverse('website:index')
        )

        self.assertTrue(
            response.wsgi_request.user.is_authenticated
        )

    def test_invalid_login(self):
        User.objects.create_user(
            username='loginuser',
            password='StrongPass123!'
        )

        response = self.client.post(
            reverse('accounts:login'),
            {
                'username': 'loginuser',
                'password': 'WrongPassword!'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        user = User.objects.create_user(
            username='logoutuser',
            password='StrongPass123!'
        )

        self.client.login(
            username='logoutuser',
            password='StrongPass123!'
        )

        response = self.client.get(
            reverse('accounts:logout')
        )

        self.assertRedirects(
            response,
            reverse('website:index')
        )

        self.assertFalse(
            response.wsgi_request.user.is_authenticated
        )

    def test_logout_requires_login(self):
        response = self.client.get(
            reverse('accounts:logout')
        )

        self.assertRedirects(
            response,
            '/accounts/login/?next=/accounts/logout/'
        )

    def test_signup_rejects_weak_password(self):
        response = self.client.post(
            reverse('accounts:signup'),
            {
                'username': 'weakuser',
                'first_name': 'Weak',
                'last_name': 'User',
                'email': 'weak@example.com',
                'password1': '123',
                'password2': '123',
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            User.objects.filter(username='weakuser').exists()
        )

class AuthorDashboardTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='normaluser',
            password='StrongPass123!'
        )

    def test_create_post_requires_author_permission(self):
        self.client.login(
            username='normaluser',
            password='StrongPass123!'
        )

        response = self.client.get(
            reverse('blog:create_post')
        )

        self.assertEqual(response.status_code, 403)

    def test_author_can_access_create_post(self):
        author_group = Group.objects.create(name='Authors')
        self.user.groups.add(author_group)

        self.client.login(
            username='normaluser',
            password='StrongPass123!'
        )

        response = self.client.get(
            reverse('blog:create_post')
        )

        self.assertEqual(response.status_code, 200)

    def test_author_can_create_post(self):
        author_group = Group.objects.create(name='Authors')
        self.user.groups.add(author_group)

        self.client.login(
            username='normaluser',
            password='StrongPass123!'
        )

        category = Category.objects.create(name='Technology')

        response = self.client.post(
            reverse('blog:create_post'),
            {
                'title': 'Test Created Post',
                'content': 'This post was created by a test.',
                'category': [category.id],
                'tags': 'django',
                'status': True,
                'publish_date': timezone.now(),
            }
        )

        self.assertRedirects(
            response,
            reverse('blog:dashboard')
        )

        post = Post.objects.get(title='Test Created Post')

        self.assertEqual(post.author, self.user)

    def test_author_cannot_edit_other_author_post(self):
        author_group = Group.objects.create(name='Authors')

        other_user = User.objects.create_user(
            username='otherauthor',
            password='StrongPass123!'
        )

        self.user.groups.add(author_group)
        other_user.groups.add(author_group)

        post = Post.objects.create(
            title='Other Author Post',
            content='Other author content.',
            author=other_user,
            status=True,
            publish_date=timezone.now()
        )

        self.client.login(
            username='normaluser',
            password='StrongPass123!'
        )

        response = self.client.get(
            reverse('blog:edit_post', kwargs={'pid': post.id})
        )

        self.assertEqual(response.status_code, 404)

    def test_author_can_edit_own_post(self):
        author_group = Group.objects.create(name='Authors')
        self.user.groups.add(author_group)

        post = Post.objects.create(
            title='Original Title',
            content='Original content.',
            author=self.user,
            status=True,
            publish_date=timezone.now()
        )

        self.client.login(
            username='normaluser',
            password='StrongPass123!'
        )

        category = Category.objects.create(name='Technology')

        response = self.client.post(
            reverse('blog:edit_post', kwargs={'pid': post.id}),
            {
                'title': 'Updated Title',
                'content': 'Updated content.',
                'category': [category.id],
                'tags': 'django',
                'status': True,
                'publish_date': timezone.now(),
            }
        )

        self.assertRedirects(
            response,
            reverse('blog:dashboard')
        )

        post.refresh_from_db()

        self.assertEqual(post.title, 'Updated Title')
        self.assertEqual(post.content, 'Updated content.')

    def test_author_cannot_delete_other_author_post(self):
        author_group = Group.objects.create(name='Authors')

        other_user = User.objects.create_user(
            username='otherauthor',
            password='StrongPass123!'
        )

        self.user.groups.add(author_group)
        other_user.groups.add(author_group)

        post = Post.objects.create(
            title='Other Author Post',
            content='Other author content.',
            author=other_user,
            status=True,
            publish_date=timezone.now()
        )

        self.client.login(
            username='normaluser',
            password='StrongPass123!'
        )

        response = self.client.get(
            reverse('blog:delete_post', kwargs={'pid': post.id})
        )

        self.assertEqual(response.status_code, 404)

    def test_author_can_delete_own_post(self):
        author_group = Group.objects.create(name='Authors')
        self.user.groups.add(author_group)
    
        post = Post.objects.create(
            title='Post To Delete',
            content='This post will be deleted.',
            author=self.user,
            status=True,
            publish_date=timezone.now()
        )
    
        self.client.login(
            username='normaluser',
            password='StrongPass123!'
        )
    
        response = self.client.post(
            reverse('blog:delete_post', kwargs={'pid': post.id})
        )
    
        self.assertRedirects(
            response,
            reverse('blog:dashboard')
        )
    
        self.assertFalse(
            Post.objects.filter(id=post.id).exists()
        )