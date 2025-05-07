from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
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
        self.client = APIClient()
        self.client.login(username="testuser", password="testpassword")

    def test_detail_question(self):
        url = reverse('question-detail', kwargs={'pk': self.question.id})
        response = self.client.get(url)
        expacted_data = QuestionSerializer(self.question).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expacted_data)
        self.assertContains(response, 'title')

        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Question.objects.get().author, self.user)


    # def test_list_post_question(self):
    #     url = reverse('question-list')
    #     data= {'title':'Question1',
    #             'content':'Content1',
    #             'author':self.user.id,
    #             'category':'frontend'}
        
    #     response = self.client.post(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
