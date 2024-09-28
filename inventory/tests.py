

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Item
from rest_framework_simplejwt.tokens import RefreshToken

class ItemTests(APITestCase):
    def setUp(self):
        self.item_data = {'name': 'Test Item', 'description': 'A test item description.'}
        self.item = Item.objects.create(**self.item_data)
        self.user = self.client.post('/api/token/', {'username': 'admin', 'password': 'password'}).data
        self.token = self.user['access']

    def test_create_item(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post('/api/items/', self.item_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_item(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(f'/api/items/{self.item.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        new_data = {'name': 'Updated Item', 'description': 'Updated description.'}
        response = self.client.put(f'/api/items/{self.item.id}/', new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_item(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(f'/api/items/{self.item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

