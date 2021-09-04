from datetime import timedelta
from django.test import TestCase
from .models import Tweet
from django.contrib.auth.models import User
from utils.time_helpers import utc_now

class TweetTests(TestCase):
    def test_hours_to_now(self):
        new_user = User.objects.create_user("liquan")
        new_tweet = Tweet.objects.create(user = new_user, content = "good day mate")
        new_tweet.created_at = utc_now() - timedelta(hours=10)
        new_tweet.save()
        self.assertEqual(new_tweet.hours_to_now, 10)

