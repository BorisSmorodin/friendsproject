from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser, FriendRequest, Friends
import json


class TestLists(APITestCase):

    def setUp(self) -> None:
        test_user_1 = CustomUser()
        test_user_1.username = "TestUser1"
        test_user_1.save()
        test_user_2 = CustomUser()
        test_user_2.username = "TestUser2"
        test_user_2.save()
        test_user_3 = CustomUser()
        test_user_3.username = "TestUser3"
        test_user_3.save()

        test_request_1 = FriendRequest()
        test_request_1.status, test_request_1.from_user, test_request_1.to_user = 1, test_user_1, test_user_2
        test_request_1.save()
        test_request_2 = FriendRequest()
        test_request_2.status, test_request_2.from_user, test_request_2.to_user = 1, test_user_1, test_user_3
        test_request_2.save()
        test_request_3 = FriendRequest()
        test_request_3.status, test_request_3.from_user, test_request_3.to_user = 1, test_user_3, test_user_2
        test_request_3.save()

        test_friends_1 = Friends()
        test_friends_1.user_1, test_friends_1.user_2 = test_user_1, test_user_2
        test_friends_1.save()
        test_friends_2 = Friends()
        test_friends_2.user_1, test_friends_2.user_2 = test_user_1, test_user_3
        test_friends_2.save()
        test_friends_3 = Friends()
        test_friends_3.user_1, test_friends_3.user_2 = test_user_3, test_user_2
        test_friends_3.save()

    def test_registration(self):
        url = "/api/register/"
        data = {
            "username": "TestUser4"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 4)
        self.assertEqual(json.loads(response.content), {"id": 4, "username": "TestUser4"})

        url = "/api/register/"
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 4)

        url = "/api/register/"
        data = {"username": ""}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 4)
