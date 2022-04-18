from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from comments.models import Comment
from testing.testcases import TestCase
from tweets.models import Tweet

# end with '/', otherwise there will be 301 redirect
COMMENT_CREATE_API = '/api/comments/'
COMMENT_DETAIL_API = '/api/comments/{}/'
COMMENT_LIST_API = '/api/comments/'


class CommentAPITests(TestCase):

    def setUp(self):
        self.user1 = self.create_user('liquan','liquan@gg.com','12345678')
        self.tweet = self.create_tweet(self.user1)

        self.user1_client = APIClient()
        self.user1_client.force_authenticate(user=self.user1)

        self.user2 = self.create_user('liquan2', 'liquan2@gg.com', '12345678')
        self.user2_client = APIClient()
        self.user2_client.force_authenticate(user=self.user2)


    def test_list_api(self):
        # have to provide tweet_id
        response = self.anonymous_client.get(COMMENT_LIST_API)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # normal request
        # no error
        # at the beginning, there is no comment
        response = self.anonymous_client.get(COMMENT_LIST_API, {'tweet_id': self.tweet.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['comments']), 0)

        self.comment1 = self.create_comment(self.user1, self.tweet, "comment1")
        self.comment2 = self.create_comment(self.user1, self.tweet, "comment2")

        response = self.anonymous_client.get(COMMENT_LIST_API, {'tweet_id': self.tweet.id})
        # ensure the data is order by the created_at
        self.assertEqual(response.data['comments'][1]['id'], self.comment2.id)
        self.assertEqual(response.data['comments'][0]['id'], self.comment1.id)


    def test_create_api(self):
        # have to login to create comments
        response = self.anonymous_client.post(
            COMMENT_CREATE_API,
            {'tweet_id': self.tweet.id,'content': 'test comment 1'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # have to provide tweet_id and content
        response = self.user1_client.post(COMMENT_CREATE_API)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # tweet only
        response = self.user1_client.post(COMMENT_CREATE_API, {'tweet_id': self.tweet.id})
        self.assertEqual(response.status_code, 400)

        # content only
        response = self.user1_client.post(COMMENT_CREATE_API, {'content': '1'})
        self.assertEqual(response.status_code, 400)

        # too long content
        response = self.user1_client.post(
            COMMENT_CREATE_API,
            {'tweet_id': self.tweet.id,'content': '1' * 200}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # create a comment successfully
        comments_count = Comment.objects.count()
        response = self.user1_client.post(
            COMMENT_CREATE_API,
            {'tweet_id': self.tweet.id,'content': 'test comment 1'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['username'], self.user1.username)
        self.assertEqual(response.data['tweet_id'], self.tweet.id)
        self.assertEqual(Comment.objects.count(), comments_count + 1)


    def test_destroy_api(self):
        comment = self.create_comment(self.user1, self.tweet)
        url =  COMMENT_DETAIL_API.format(comment.id)

        # have to login to destroy comments
        response = self.anonymous_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # have to be the owner of the tweet
        response = self.user2_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        # delete a comment successfully
        comments_count = Comment.objects.count()
        response = self.user1_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), comments_count - 1)

    def test_update_api(self):
        comment = self.create_comment(self.user1, self.tweet)
        url =  COMMENT_DETAIL_API.format(comment.id)

        # have to login to destroy comments
        response = self.anonymous_client.put(
            url,
            {'content': 'modified content'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # have to be the owner of the tweet
        response = self.user2_client.put(
            url,
            {'content': 'modified content'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # content too long
        response = self.user1_client.put(
            url,
            {'content': '1' * 200},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # update a comment successfully
        before_updated_at = comment.updated_at
        before_created_at = comment.created_at
        now = timezone.now()
        comments_count = Comment.objects.count()
        response = self.user1_client.put(
            url,
            {
                'content': 'modified content',
                'user_id': self.user2.id,
                'tweet_id': 3,
                'created_at': now,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(response.data['content'], 'modified content')
        self.assertEqual(Comment.objects.count(), comments_count)
        self.assertEqual(comment.user, self.user1)
        self.assertEqual(comment.tweet, self.tweet)
        self.assertEqual(comment.created_at, before_created_at)
        self.assertNotEqual(comment.created_at, now)
        self.assertNotEqual(comment.updated_at, before_updated_at)
