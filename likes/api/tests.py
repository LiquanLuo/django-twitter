from rest_framework import status

from testing.testcases import TestCase

# end with '/', otherwise there will be 301 redirect
LIKE_BASE_API = '/api/likes/'
LIKE_CANCEL_API = '/api/likes/cancel/'


class LikeAPITests(TestCase):

    def setUp(self):
        self.user1, self.user1_client = self.create_user_client('liquan1','liquan@gg.com','12345678')
        self.user2, self.user2_client = self.create_user_client('liquan2', 'liquan2@gg.com', '12345678')

    def test_tweet_like(self):
        tweet = self.create_tweet(self.user1)
        data = {'content_type': 'tweet', 'object_id': tweet.id}

        # anonymous is not allowed
        response = self.anonymous_client.post(LIKE_BASE_API, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # get is not allowed
        response = self.user1_client.get(LIKE_BASE_API, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # post success
        response = self.user1_client.post(LIKE_BASE_API, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(tweet.like_set.count(), 1)

        # duplicate like
        response = self.user1_client.post(LIKE_BASE_API, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(tweet.like_set.count(), 1)

        # two clients like same tweet
        response = self.user2_client.post(LIKE_BASE_API, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(tweet.like_set.count(), 2)


    def test_comment_like(self):
        tweet = self.create_tweet(self.user1)
        comment = self.create_comment(self.user2, tweet)
        data = {'content_type': 'comment', 'object_id': comment.id}

        # anonymous is not allowed
        response = self.anonymous_client.post(LIKE_BASE_API, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # get is not allowed
        response = self.user1_client.get(LIKE_BASE_API, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # wrong content_type
        response = self.user1_client.post(LIKE_BASE_API, {'content_type': 'twitter', 'object_id': comment.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('content_type' in response.data['errors'], True)

        # wrong object id
        response = self.user1_client.post(LIKE_BASE_API, {'content_type': 'comment', 'object_id': -1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('object_id' in response.data['errors'], True)

        # post success
        response = self.user1_client.post(LIKE_BASE_API, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment.like_set.count(), 1)

        # duplicate like
        response = self.user1_client.post(LIKE_BASE_API, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment.like_set.count(), 1)

        # two clients like same tweet
        response = self.user2_client.post(LIKE_BASE_API, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment.like_set.count(), 2)

    def test_cancel(self):
        tweet = self.create_tweet(self.user1)
        comment = self.create_comment(self.user2, tweet)
        like_tweet_data = {'content_type': 'tweet', 'object_id' : tweet.id}
        like_comment_data = {'content_type': 'comment', 'object_id' : comment.id}
        self.user1_client.post(LIKE_BASE_API, like_tweet_data)
        self.user2_client.post(LIKE_BASE_API, like_comment_data)
        self.assertEqual(tweet.like_set.count(), 1)
        self.assertEqual(comment.like_set.count(), 1)

        # login required
        response = self.anonymous_client.post(LIKE_CANCEL_API, like_tweet_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # get is not allowed
        response = self.user1_client.get(LIKE_CANCEL_API, like_tweet_data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # wrong content_type
        response = self.user1_client.post(LIKE_CANCEL_API, {'content_type': 'twitter', 'object_id' : tweet.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # print(response.data)

        # wrong object_id
        response = self.user1_client.post(LIKE_CANCEL_API, {'content_type': 'tweet', 'object_id': -1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # user1 has not liked comment before
        response = self.user1_client.post(LIKE_CANCEL_API, like_comment_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tweet.like_set.count(), 1)
        self.assertEqual(comment.like_set.count(), 1)

        # successfully canceled tweet like
        response = self.user1_client.post(LIKE_CANCEL_API, like_tweet_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tweet.like_set.count(), 0)
        self.assertEqual(comment.like_set.count(), 1)

        # user2 has not liked tweet before
        response = self.user2_client.post(LIKE_CANCEL_API, like_tweet_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tweet.like_set.count(), 0)
        self.assertEqual(comment.like_set.count(), 1)


        # user2's comment like has been canceled
        response = self.user2_client.post(LIKE_CANCEL_API, like_comment_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tweet.like_set.count(), 0)
        self.assertEqual(comment.like_set.count(), 0)