from django.contrib.auth.models import User
from rest_framework import serializers, exceptions
from accounts.api.serializers import UserSerializer
from friendships.models import Friendship


class FollowerSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='from_user')
    class Meta:
        model = Friendship
        fields = ('user','created_at',)

class FollowingSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='to_user')
    class Meta:
        model = Friendship
        fields = ('user','created_at',)


class FriendshipCreateSerializer(serializers.ModelSerializer):
    from_user_id = serializers.IntegerField()
    to_user_id = serializers.IntegerField()

    class Meta:
        model = Friendship
        fields = ('from_user_id', 'to_user_id')

    def validate(self, data):
        if data['from_user_id'] == data['to_user_id']:
            raise exceptions.ValidationError({
                'message': 'cannot follow yourself'
            })
        if not User.objects.filter(id=data['to_user_id']).exists():
            raise exceptions.ValidationError({
                'message': 'cannot follow non-exist user'
            })
        return data

    def create(self, validated_data):
        from_user_id = validated_data['from_user_id']
        to_user_id = validated_data['to_user_id']

        friendship = Friendship.objects.create(
            from_user_id = from_user_id,
            to_user_id = to_user_id
        )
        return friendship