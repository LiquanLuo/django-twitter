from rest_framework import serializers, exceptions

from accounts.api.serializers import UserSerializer
from comments.models import Comment
from tweets.models import Tweet


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = ('id', 'user', 'tweet_id', 'content', 'created_at', 'updated_at')


class CommentCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    tweet_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ('user_id', 'tweet_id', 'content',)

    def validate(self, data):
        if not Tweet.objects.filter(id = data['tweet_id']).exists():
            raise exceptions.ValidationError({
                'message': 'cannot find this tweet'
            })

        return data

    def create(self, validated_data):
        user_id = validated_data['user_id']
        tweet_id = validated_data['tweet_id']
        content = validated_data['content']
        comment = Comment.objects.create(user_id = user_id, tweet_id = tweet_id, content = content)
        return comment


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)

    def update(self, instance, validated_data):
        instance.content = validated_data['content']
        instance.save()
        return instance