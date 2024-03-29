from django.contrib.contenttypes.models import ContentType
from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from tweets.models import Tweet
from comments.models import Comment
from likes.models import Like
from newsfeeds.models import Newsfeed

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

    def create_newsfeed(self, user, tweet):
        return Newsfeed.objects.create(user = user, tweet = tweet)

    def create_comment(self, user, tweet, content=None):
        if content is None:
            content = 'default comment content'
        return Comment.objects.create(user=user, tweet=tweet, content=content)

    def create_like(self, user, target):
        instance, _ =  Like.objects.get_or_create(
            user=user,
            content_type = ContentType.objects.get_for_model(target.__class__),
            object_id = target.id,
        )

        return instance

    def create_user_client(self, username, email="None2343", password="123456"):
        user = self.create_user(username, email, password)
        client = APIClient()
        client.force_authenticate(user=user)

        return user, client