from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Question
from .api.serializers import QuestionSerializer
from django.contrib.auth.models import User



class LikeTests(APITestCase):

    def test_get_like(self):
        url = reverse('like-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class QuestionTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.question = Question.objects.create(title='Test Question', content='Test Content', author=self.user, category='frontend')
        pass


    def test_detail_question(self):
        pass
