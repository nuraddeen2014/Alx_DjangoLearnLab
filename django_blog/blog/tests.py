from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post, Comment


class CommentPermissionsTests(TestCase):
	def setUp(self):
		User = get_user_model()
		self.user1 = User.objects.create_user(username='user1', password='pass')
		self.user2 = User.objects.create_user(username='user2', password='pass')
		self.post = Post.objects.create(title='Hello', content='Content', author=self.user1)
		self.comment = Comment.objects.create(post=self.post, author=self.user1, content='Nice post')

	def test_author_can_edit_comment(self):
		self.client.login(username='user1', password='pass')
		url = reverse('comment-update', kwargs={'pk': self.comment.pk})
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

		response = self.client.post(url, {'content': 'Updated content'})
		# After a successful update we redirect to the comment list
		self.assertEqual(response.status_code, 302)
		self.comment.refresh_from_db()
		self.assertEqual(self.comment.content, 'Updated content')

	def test_non_author_cannot_edit_comment(self):
		self.client.login(username='user2', password='pass')
		url = reverse('comment-update', kwargs={'pk': self.comment.pk})
		response = self.client.get(url)
		# We expect a redirect to post-detail due to permission check override
		self.assertEqual(response.status_code, 302)

	def test_author_can_delete_comment(self):
		self.client.login(username='user1', password='pass')
		url = reverse('comment-delete', kwargs={'pk': self.comment.pk})
		response = self.client.post(url)
		self.assertEqual(response.status_code, 302)
		self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

	def test_non_author_cannot_delete_comment(self):
		self.client.login(username='user2', password='pass')
		url = reverse('comment-delete', kwargs={'pk': self.comment.pk})
		response = self.client.post(url)
		self.assertEqual(response.status_code, 302)
		# Comment should still exist
		self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())


# Create your tests here.
