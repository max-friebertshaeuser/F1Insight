# from django.urls import reverse
# from rest_framework.test import APITestCase, APIClient
# from django.contrib.auth.models import User
# from .models import Group
# from rest_framework import status
# from django.utils import timezone
#
#
# class GroupEndpointsTestCase(APITestCase):
#     def setUp(self):
#         self.owner = User.objects.create_user(username='owner', password='pass')
#         self.member = User.objects.create_user(username='member', password='pass')
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.owner)
#
#         self.group = Group.objects.create(
#             owner=self.owner,
#             name='TestGroup',
#             created_at=timezone.now()
#         )
#         self.group.members.add(self.owner)
#
#     def test_create_group(self):
#         url = reverse('create_group')
#         data = {
#             'name': 'owner',
#             'group_name': 'NewGroup',
#             'members': ['member']
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['status'], 'group created')
#
#     def test_create_group_owner_not_found(self):
#         url = reverse('create_group')
#         data = {
#             'name': 'notfound',
#             'group_name': 'AnotherGroup',
#             'members': []
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_create_group_already_exists(self):
#         url = reverse('create_group')
#         data = {
#             'name': 'owner',
#             'group_name': 'TestGroup',
#             'members': []
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_join_group(self):
#         url = reverse('join_group')
#         self.client.force_authenticate(user=self.member)
#         data = {'group_name': 'TestGroup'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['status'], 'joined group successfully')
#
#     def test_join_group_not_found(self):
#         url = reverse('join_group')
#         self.client.force_authenticate(user=self.member)
#         data = {'group_name': 'NoGroup'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_leave_group(self):
#         self.group.members.add(self.member)
#         url = reverse('leave_group')
#         self.client.force_authenticate(user=self.member)
#         data = {'group_name': 'TestGroup'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['status'], 'left group successfully')
#
#     def test_leave_group_not_found(self):
#         url = reverse('leave_group')
#         self.client.force_authenticate(user=self.member)
#         data = {'group_name': 'NoGroup'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_get_all_groups(self):
#         url = reverse('get_all_groups')
#         response = self.client.post(url, {}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['status'], 'success')
#         self.assertTrue('groups' in response.data)
#         self.assertEqual(len(response.data['groups']), 1)
#
#     def test_remove_group(self):
#         url = reverse('remove_group')
#         data = {'group_id': self.group.id}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['status'], 'group deleted successfully')
#
#     def test_remove_group_not_owner(self):
#         url = reverse('remove_group')
#         self.client.force_authenticate(user=self.member)
#         data = {'group_id': self.group.id}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_remove_group_not_found(self):
#         url = reverse('remove_group')
#         data = {'group_id': 9999}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)