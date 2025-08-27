from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.utils import timezone
from .models import Task

# Create your tests here.
User = get_user_model()

class TaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='p')
        self.client = APIClient()
        self.client.login(username='u1', password='p')

    def test_create_and_mark_complete_and_block_edit(self):
        resp = self.client.post('/api/task/', {
            'title':'t',
            'description':'d',
            'due_date': (timezone.now() + timezone.timedelta(days=1)).isoformat(),
            'priority':'low'
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        task_id = resp.data['id']

        # mark complete
        resp = self.client.post(f'/api/task/{task_id}/mark-complete/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['status'],'completed')
        self.assertIsNotNone(resp.data['completed_at'])

        # attempt edit -> should fail
        resp = self.client.patch(f'/api/task/{task_id}/', {'title':'new'}, format='json')
        self.assertEqual(resp.status_code, 400)