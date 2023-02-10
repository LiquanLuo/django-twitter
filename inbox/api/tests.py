from notifications.models import Notification
from rest_framework import status

from testing.testcases import TestCase

COMMENT_URL = '/api/comments/'
LIKE_URL = '/api/likes/'
NOTIFICATION_URL = '/api/notifications/'

class NotificationTests(TestCase):
    def setUp(self) -> None:
        self.user1, self.user1_client = self.create_user_client("liquan")
        self.user2, self.user2_client = self.create_user_client("liquan2")
        self.user1_tweet = self.create_tweet(self.user1)

    def test_comment_creat_api_notification(self):
        self.assertEqual(Notification.objects.count(), 0)
        self.user2_client.post(COMMENT_URL, {
            'tweet_id': self.user1_tweet.id,
            'content': 'test comment',
        })
        self.assertEqual(Notification.objects.count(), 1)

    def test_like_creat_api_notification(self):
        self.assertEqual(Notification.objects.count(), 0)
        self.user2_client.post(LIKE_URL, {
            'content_type': 'tweet',
            'object_id': self.user1_tweet.id,
        })
        self.assertEqual(Notification.objects.count(), 1)

class NotificationAPITests(TestCase):
    def setUp(self) -> None:
        self.user1, self.user1_client = self.create_user_client("liquan")
        self.user2, self.user2_client = self.create_user_client("liquan2")
        self.user1_tweet = self.create_tweet(self.user1)

    def test_unread_count(self):
        # unread like
        self.user2_client.post(LIKE_URL, {
            'content_type': 'tweet',
            'object_id': self.user1_tweet.id,
        })
        url = NOTIFICATION_URL + 'unread-count/'
        response = self.user1_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['unread_count'], 1)

        # unread comment
        self.user2_client.post(COMMENT_URL, {
            'tweet_id': self.user1_tweet.id,
            'content': 'test comment',
        })
        response = self.user1_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['unread_count'], 2)

    def test_mark_all_as_read(self):
        self.user2_client.post(LIKE_URL, {
            'content_type': 'tweet',
            'object_id': self.user1_tweet.id,
        })
        self.user2_client.post(COMMENT_URL, {
            'tweet_id': self.user1_tweet.id,
            'content': 'test comment',
        })

        unread_url = NOTIFICATION_URL + 'unread-count/'
        response = self.user1_client.get(unread_url)
        self.assertEqual(response.data['unread_count'], 2)

        mark_url = NOTIFICATION_URL + 'mark-all-as-read/'

        # get not allowed
        response = self.user1_client.get(mark_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # mark 2 unread as read
        response = self.user1_client.post(mark_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['updated_count'], 2)
        response = self.user1_client.get(unread_url)
        self.assertEqual(response.data['unread_count'], 0)

    def test_list(self):
        self.user2_client.post(LIKE_URL, {
            'content_type': 'tweet',
            'object_id': self.user1_tweet.id,
        })
        self.user2_client.post(COMMENT_URL, {
            'tweet_id': self.user1_tweet.id,
            'content': 'test comment',
        })

        # anonymous cannot acccess
        response = self.anonymous_client.get(NOTIFICATION_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # user 2 do not have any notification
        response = self.user2_client.get(NOTIFICATION_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        # user 1 has two notifications
        response = self.user1_client.get(NOTIFICATION_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        # mark 1 as read
        notification = self.user1.notifications.first()
        notification.unread = False
        notification.save()
        response = self.user1_client.get(NOTIFICATION_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        response = self.user1_client.get(NOTIFICATION_URL, {'unread': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        response = self.user1_client.get(NOTIFICATION_URL, {'unread': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_update(self):
        self.user2_client.post(LIKE_URL, {
            'content_type': 'tweet',
            'object_id': self.user1_tweet.id,
        })
        self.user2_client.post(COMMENT_URL, {
            'tweet_id': self.user1_tweet.id,
            'content': 'test comment',
        })
        notification = self.user1.notifications.first()

        url = '/api/notifications/{}/'.format(notification.id)

        # cannot use post, have to use put
        response = self.user1_client.post(url, {'unread':False})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # cannot use anonymouse
        response = self.anonymous_client.put(url, {'unread':False})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # other user cannot access this notification
        response = self.user2_client.put(url, {'unread': False})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # successfully update this notification
        response = self.user1_client.put(url, {'unread': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        unread_url = '/api/notifications/unread-count/'
        response = self.user1_client.get(unread_url)
        self.assertEqual(response.data['unread_count'], 1)

        # mark it as unread
        self.user1_client.put(url, {'unread': True})
        response = self.user1_client.get(unread_url)
        self.assertEqual(response.data['unread_count'], 2)

        # have to contain unread
        response = self.user1_client.put(url, {'verb': 'newverb'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # cannot modify other info
        response = self.user1_client.put(url, {'verb': 'newverb', 'unread': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notification.refresh_from_db()
        self.assertNotEqual(notification.verb, 'newverb')