from rest_framework import status
from rest_framework.test import APIClient

from friendships.models import Friendship
from testing.testcases import TestCase

FRIENDSHIP_FOLLOW_API = '/api/friendships/{}/follow/'
FRIENDSHIP_UNFOLLOW_API = '/api/friendships/{}/unfollow/'
FRIENDSHIP_FOLLOWINGS_API = '/api/friendships/{}/followings/'
FRIENDSHIP_FOLLOWERS_API = '/api/friendships/{}/followers/'


class FriednshipAPITests(TestCase):

    def setUp(self):
        self.user1 = self.create_user('liquan','liquan@gg.com','12345678')
        self.tweets1 = [
            self.create_tweet(self.user1)
            for i in range(3)
        ]

        self.user1_client = APIClient()
        self.user1_client.force_authenticate(user=self.user1)

        self.user2 = self.create_user('liquan2', 'liquan2@gg.com', '12345678')
        self.user2_client = APIClient()
        self.user2_client.force_authenticate(user=self.user2)


    def test_follow_api(self):
        # have to log in
        response = self.anonymous_client.post(FRIENDSHIP_FOLLOW_API.format(self.user2.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # have to use post method
        response = self.user1_client.get(FRIENDSHIP_FOLLOW_API.format(self.user2.id))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # cannot follow yourself
        response = self.user1_client.post(FRIENDSHIP_FOLLOW_API.format(self.user1.id))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # cannot follow non-exist user
        response = self.user1_client.post(FRIENDSHIP_FOLLOW_API.format(100))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # normal request
        response = self.user1_client.post(FRIENDSHIP_FOLLOW_API.format(self.user2.id))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('friendship' in response.data, True)
        self.assertEqual(response.data['friendship']['from_user_id'], self.user1.id)
        self.assertEqual(response.data['friendship']['to_user_id'], self.user2.id)

        # duplicate request
        response = self.user1_client.post(FRIENDSHIP_FOLLOW_API.format(self.user2.id))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['duplicate'], True)

        # follow back
        count = Friendship.objects.count()
        response = self.user2_client.post(FRIENDSHIP_FOLLOW_API.format(self.user1.id))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Friendship.objects.count(), count + 1)

    def test_unfollow_api(self):
        response = self.user1_client.post(FRIENDSHIP_FOLLOW_API.format(self.user2.id))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = FRIENDSHIP_UNFOLLOW_API.format(self.user2.id)

        # have to log in
        response = self.anonymous_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # have to use post method
        response = self.user1_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # cannot unfollow yourself
        response = self.user1_client.post(FRIENDSHIP_UNFOLLOW_API.format(self.user1.id))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # unfollow non-exist user
        response = self.user1_client.post(FRIENDSHIP_UNFOLLOW_API.format(100))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['deleted'], 0)

        # normal request
        response = self.user1_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['deleted'], 1)

        # duplicate request
        response = self.user1_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['deleted'], 0)

    def test_followings_api(self):
        for i in range(2):
            following = self.create_user('user1_following{}'.format(i))
            Friendship.objects.create(from_user=self.user1, to_user=following)

        url = FRIENDSHIP_FOLLOWINGS_API.format(self.user1.id)

        # have to use GET method
        response = self.user1_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # normal request
        response = self.user1_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # make sure its ordered by created_at
        ts0 = response.data['followings'][0]['created_at']
        ts1 = response.data['followings'][1]['created_at']
        self.assertEqual(ts0 > ts1, True)
        self.assertEqual(
            response.data['followings'][0]['user']['username'],
            'user1_following1',
        )
        self.assertEqual(
            response.data['followings'][1]['user']['username'],
            'user1_following0',
        )

    def test_followers_api(self):
        for i in range(3):
            follower = self.create_user('user1_follower{}'.format(i))
            Friendship.objects.create(from_user=follower, to_user=self.user1)

        url = FRIENDSHIP_FOLLOWERS_API.format(self.user1.id)

        # have to use GET method
        response = self.user1_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # normal request
        response = self.user1_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # make sure its ordered by created_at
        ts0 = response.data['followers'][0]['created_at']
        ts1 = response.data['followers'][1]['created_at']
        ts2 = response.data['followers'][2]['created_at']
        self.assertEqual(ts0 > ts1, True)
        self.assertEqual(ts1 > ts2, True)
        self.assertEqual(
            response.data['followers'][0]['user']['username'],
            'user1_follower2',
        )
        self.assertEqual(
            response.data['followers'][1]['user']['username'],
            'user1_follower1',
        )
        self.assertEqual(
            response.data['followers'][2]['user']['username'],
            'user1_follower0',
        )


