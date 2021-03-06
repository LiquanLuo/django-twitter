from accounts.api.serializers import UserSerializer
from rest_framework import serializers
from tweets.models import Tweet
from comments.api.serializers import CommentSerializer


class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Tweet
        fields = ('id', 'user', 'content', 'created_at',)


class TweetCreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=140, min_length=6)

    class Meta:
        model = Tweet
        fields = ('content',)

    def create(self, validated_data):
        user = self.context['request'].user
        content = validated_data['content']
        tweet = Tweet.objects.create(user = user,content = content)
        return tweet

class TweetSerializerWithComments(serializers.ModelSerializer):
    user = UserSerializer()
    comments = CommentSerializer(source='comment_set', many=True)
    class Meta:
        model = Tweet
        fields = ('id', 'user', 'comments', 'content', 'created_at',)