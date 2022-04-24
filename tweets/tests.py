from datetime import timedelta
from testing.testcases import TestCase
from .models import Tweet
from utils.time_helpers import utc_now

class TweetTests(TestCase):
    def setUp(self) -> None:
        self.user1 = self.create_user('liquan', 'liquan@gg.com', '12345678')
        self.tweets1 = self.create_tweet(self.user1)
        self.user2 = self.create_user('liquan2', "adfsdf@gg.com","ddddd")

    def test_hours_to_now(self):
        new_tweet = Tweet.objects.create(user = self.user1, content = "good day mate")
        new_tweet.created_at = utc_now() - timedelta(hours=10)
        new_tweet.save()
        self.assertEqual(new_tweet.hours_to_now, 10)

    def test_like_set(self):
        # no like at the beginning
        self.assertEqual(len(self.tweets1.like_set), 0)

        # successfully like a tweet
        self.create_like(self.user1, self.tweets1)
        self.assertEqual(len(self.tweets1.like_set), 1)

        # like the same tweet, it won't change the anything
        self.create_like(self.user1, self.tweets1)
        self.assertEqual(len(self.tweets1.like_set), 1)

        # someone else like the same tweet, the count increase
        self.create_like(self.user2, self.tweets1)
        self.assertEqual(len(self.tweets1.like_set), 2)





