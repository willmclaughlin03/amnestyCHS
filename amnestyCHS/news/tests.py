from django.test import TestCase
from .models import News
from django.urls import reverse

class NewsModelTest(TestCase):

    def test_slug_generation(self):
        news = News.objects.create(title =   "Test News", content = 'Test Content')

        self.assertEqual(news.slug, ("test-news"))

    def test_str_returns_a_title(self):
        news = News.objects.create(title = "Test Title", content = 'Testing the title of the post')

        self.assertEqual(str(news), "Test Title")
"""
     def test_unauthenticated_user_cannot_create_news(self):
        self.client.logout()
        response = self.client.get(reverse("news_create"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/')) """
# undecided on how to address admin login at this point 