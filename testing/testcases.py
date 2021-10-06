from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from tweets.models import Tweet

class TestCase(DjangoTestCase):

    @property
    def anonymous_client(self):
        if not hasattr(self, '_anonymous_client'):
            self._anonymous_client = APIClient()
        return self._anonymous_client


    def create_user(self, username, email="None2343", password="123456"):
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

