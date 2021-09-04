from rest_framework import status
from rest_framework.test import APIClient
from testing.testcases import TestCase
from tweets.models import Tweet

# end with '/', otherwise there will be 301 redirect
TWEET_LIST_API = '/api/tweets/'
TWEET_CREATE_API = '/api/tweets/'


class TweetAPITests(TestCase):

    def setUp(self):
        self.anonymous_client = APIClient()

        self.user1 = self.create_user('liquan','liquan@gg.com','12345678')
        self.tweets1 = [
            self.create_tweet(self.user1)
            for i in range(3)
        ]

        self.user1_client = APIClient()
        self.user1_client.force_authenticate(user=self.user1)

        self.user2 = self.create_user('liquan2', 'liquan2@gg.com', '12345678')
        self.tweets2 = [
            self.create_tweet(self.user2)
            for i in range(2)
        ]

    def test_list_api(self):
        # have to provide user_id
        response = self.anonymous_client.get(TWEET_LIST_API)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # normal request
        response = self.anonymous_client.get(TWEET_LIST_API, {'user_id': self.user1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['tweets']),3)

        response = self.anonymous_client.get(TWEET_LIST_API, {'user_id': self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['tweets']), 2)

        # ensure the data is order by the created_at
        self.assertEqual(response.data['tweets'][0]['id'], self.tweets2[1].id)
        self.assertEqual(response.data['tweets'][1]['id'], self.tweets2[0].id)
        # print(response.data)
        # print(self.tweets2)

    def test_create_api(self):
        # have to login to create tweets
        response = self.anonymous_client.post(TWEET_CREATE_API, {'content': 'test tweet 1'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # have to provide content
        response = self.user1_client.post(TWEET_CREATE_API)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # too short content
        response = self.user1_client.post(TWEET_CREATE_API,{'content':'1'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # too long content
        response = self.user1_client.post(TWEET_CREATE_API, {'content': '1'*200})
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # create a tweet successfully
        tweets_count = Tweet.objects.count()
        response = self.user1_client.post(TWEET_CREATE_API, {'content': 'a good tweet'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['username'], self.user1.username)
        self.assertEqual(Tweet.objects.count(), tweets_count + 1)