from notifications.models import Notification

from testing.testcases import TestCase

COMMENT_URL = '/api/comments/'
LIKE_URL = '/api/likes/'

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