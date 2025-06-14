from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from betting.models import Group
from rest_framework import status
from django.utils import timezone


class GroupEndpointsTestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='pass')
        self.member = User.objects.create_user(username='member', password='pass')
        self.client = APIClient()

        self.client.force_authenticate(user=self.owner)
        self.group = Group.objects.create(name='TestGroup', owner=self.owner, created_at=timezone.now())
        self.group.members.set([self.owner])

    def test_create_group_success(self):
        url = reverse('create_group')
        data = {
            'name': 'owner',
            'group_name': 'NewGroup',
            'members': ['member']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'group created')

    def test_create_group_already_exists(self):
        url = reverse('create_group')
        data = {
            'name': 'owner',
            'group_name': 'TestGroup',  # Already exists
            'members': []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['status'], 'group already exists')

    def test_create_group_owner_not_found(self):
        url = reverse('create_group')
        data = {
            'name': 'nonexistent',
            'group_name': 'AnotherGroup',
            'members': []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['status'], 'owner not found')

    def test_join_group_success(self):
        url = reverse('join_group')
        self.client.force_authenticate(user=self.member)
        data = {'group_name': 'TestGroup'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'joined group successfully')
        self.assertIn(self.member, self.group.members.all())

    def test_join_group_not_found(self):
        url = reverse('join_group')
        self.client.force_authenticate(user=self.member)
        data = {'group_name': 'NoSuchGroup'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['status'], 'group not found')

    def test_leave_group_success(self):
        self.group.members.add(self.member)
        url = reverse('leave_group')
        self.client.force_authenticate(user=self.member)
        data = {'group_name': 'TestGroup'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'left group successfully')
        self.assertNotIn(self.member, self.group.members.all())

    def test_leave_group_not_found(self):
        url = reverse('leave_group')
        self.client.force_authenticate(user=self.member)
        data = {'group_name': 'NoSuchGroup'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['status'], 'group not found')

    def test_get_all_groups(self):
        url = reverse('get_all_groups')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('groups', response.data)
        self.assertEqual(len(response.data['groups']), 1)

    def test_remove_group_success(self):
        url = reverse('remove_group')
        data = {'group_id': self.group.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'group deleted successfully')
        self.assertFalse(Group.objects.filter(id=self.group.id).exists())

    def test_remove_group_not_found(self):
        url = reverse('remove_group')
        data = {'group_id': 9999}  # Non-existent
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['status'], 'group not found')

    def test_remove_group_not_owner(self):
        url = reverse('remove_group')
        self.client.force_authenticate(user=self.member)
        data = {'group_id': self.group.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['status'], 'not authorized to delete this group')
