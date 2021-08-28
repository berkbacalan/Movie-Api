from multiprocessing import AuthenticationError
from pprint import pprint

from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category


class CategoryTest(APITestCase):
    def setUp(self):
        self.user = User(username='test_user', is_staff=True, is_superuser=True)
        self.user.set_password('password')
        self.user = User.objects.create_superuser('test_user', email=None, password='password')
        login = self.client.login(username = 'test_user', password = 'password')
        if login == False:
            raise AuthenticationError("Wrong username or password for user = %s" % self.user.username)

    def test_create_category(self):
        url = reverse('category-list')
        data = {"name": "Test Category"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'Test Category')
