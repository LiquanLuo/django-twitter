from accounts.api.serializers import UserSerializer
from rest_framework import serializers

from newsfeeds.models import Newsfeed
from tweets.api.serializers import TweetSerializer



class NewsfeedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    tweet = TweetSerializer()
    class Meta:
        model = Newsfeed
        fields = ('user', 'tweet',)
