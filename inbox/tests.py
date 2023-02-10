from inbox.services import NotificationService
from testing.testcases import TestCase
from notifications.models import Notification


class NotificationServiceTests(TestCase):

    def setUp(self) -> None:
        self.user1 = self.create_user("liquan")
        self.user2 = self.create_user("liquan2")
        self.tweet = self.create_tweet(self.user1)

    def test_send_comment_notification(self):
        # do not send notification if comment on his own tweet
        comment = self.create_comment(self.user1, self.tweet)
        NotificationService.send_comment_notification(comment)
        self.assertEqual(Notification.objects.count(), 0)

        # send notification
        comment = self.create_comment(self.user2, self.tweet)
        NotificationService.send_comment_notification(comment)
        self.assertEqual(Notification.objects.count(), 1)

    def test_send_like_notification(self):
        # do not send notification if like his own tweet
        like = self.create_like(self.user1, self.tweet)
        NotificationService.send_like_notification(like)
        self.assertEqual(Notification.objects.count(), 0)

        # send like notification
        like = self.create_like(self.user2, self.tweet)
        NotificationService.send_like_notification(like)
        self.assertEqual(Notification.objects.count(), 1)