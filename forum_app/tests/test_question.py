from django.urls import reverse
from datetime import datetime
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token 
from django.contrib.auth.models import User
from forum_app.models import Question, Like, Answer
from forum_app.api.serializers import QuestionSerializer, LikeSerializer, AnswerSerializer



class LikeTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.question = Question.objects.create(title='Test Question', content='Test Content', author=self.user, category='frontend')
        self.questionTwo = Question.objects.create(title='Test Question2', content='Test Content2', author=self.user, category='frontend')
        # self.client = APIClient()
        # self.client.login(username="testuser", password="testpassword")

        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key )

    def test_get_like(self):
        url = reverse('like-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_post_like(self):
        url = reverse('like-list')
        data = {'question':self.questionTwo.id,
                'created_at': datetime.now()}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detail_like(self):
        self.like = Like.objects.create(user=self.user, question=self.question)
        url = reverse('like-detail', kwargs={'pk': self.like.id})
        response = self.client.get(url)
        expacted_data = LikeSerializer(self.like).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expacted_data)


class QuestionTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.question = Question.objects.create(title='Test Question', content='Test Content', author=self.user, category='frontend')
        # self.client = APIClient()
        # self.client.login(username="testuser", password="testpassword")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_question(self):
        url = reverse('question-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_post_question(self):
        url = reverse('question-list')
        data= {'title':'Question1',
                'content':'Content1',
                'author':self.user.id,
                'category':'frontend'}
        
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detail_question(self):
        url = reverse('question-detail', kwargs={'pk': self.question.id})
        response = self.client.get(url)
        expacted_data = QuestionSerializer(self.question).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expacted_data)
        self.assertContains(response, 'title')

        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Question.objects.get().author, self.user)


class AnswerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.question = Question.objects.create(title='Test Question3', content='Test Content3', author=self.user, category='frontend')
        self.answer = Answer.objects.create(content='Test Answer', author=self.user, question=self.question)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_answer(self):
        url = reverse('answer-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # def test_list_post_answer(self):
    #     url = reverse('answer-list-create')
    #     data= {'content':'Answer2',
    #             'author':self.user.id,
    #             'question':self.question.id}
        
    #     response = self.client.post(url, data, format="json")
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detail_answer(self):
        url = reverse('answer-detail', kwargs={'pk': self.answer.id})
        response = self.client.get(url)
        expected_data = AnswerSerializer(self.answer).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
