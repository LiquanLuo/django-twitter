from rest_framework import status
from rest_framework.test import APIClient
from testing.testcases import TestCase
from tweets.models import Tweet

# end with '/', otherwise there will be 301 redirect
TWEET_CREATE_API = '/api/tweets/'
FRIENDSHIP_FOLLOW_API = '/api/friendships/{}/follow/'
NEWSFEED_LIST_API = '/api/newsfeeds/'


class TweetAPITests(TestCase):

    def setUp(self):
        self.user1 = self.create_user('liquan','liquan@gg.com','12345678')
        self.user1_client = APIClient()
        self.user1_client.force_authenticate(user=self.user1)

        self.user2 = self.create_user('liquan2', 'liquan2@gg.com', '12345678')
        self.user2_client = APIClient()
        self.user2_client.force_authenticate(user=self.user2)


    def test_list_api(self):
        # have to log in
        response = self.anonymous_client.get(NEWSFEED_LIST_API)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # have to use GET
        response = self.user1_client.post(NEWSFEED_LIST_API)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # at begining, 0 newsfeed
        response = self.user1_client.get(NEWSFEED_LIST_API)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['newsfeeds']), 0)


        # after post a tweet, user1 can see his own tweet
        self.user1_client.post(TWEET_CREATE_API, {'content': 'a good tweet'})
        response = self.user1_client.get(NEWSFEED_LIST_API)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['newsfeeds']), 1)


        # after following user2, user1 can see user2's tweet
        self.user1_client.post(FRIENDSHIP_FOLLOW_API.format(self.user2.id))
        response = self.user2_client.post(TWEET_CREATE_API, {'content': 'a good tweet2'})
        posted_tweet_id = response.data['id']
        response = self.user1_client.get(NEWSFEED_LIST_API)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['newsfeeds']), 2)
        self.assertEqual(response.data['newsfeeds'][0]['tweet']['id'], posted_tweet_id)


