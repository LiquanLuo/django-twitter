from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from tweets.models import Tweet

class TestCase(DjangoTestCase):
    def create_user(self, username, email, password):
        # do not use User.objects.create() directly
        # because password need to be encrypted , username and email need to be normalized
        return User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
    def create_tweet(self, user, content=None):
        if content is None:
            content = 'default tweet content'
        return Tweet.objects.create(user=user, content=content)

