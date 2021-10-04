from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response

from friendships.api.serializers import FollowerSerializer, FollowingSerializer, FriendshipCreateSerializer
from friendships.models import Friendship


class FriendshipViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = FriendshipCreateSerializer

    @action(methods=['GET'], detail=True, permission_classes=[AllowAny])
    def followers(self, request, pk):
        friendships = Friendship.objects.filter(to_user=pk).order_by('-created_at')
        serializer = FollowerSerializer(friendships, many=True)

        # normally, response has to be a hash instead of a list
        return Response({'followers': serializer.data})

    @action(methods=['GET'], detail=True, permission_classes=[AllowAny])
    def followings(self, request, pk):
        friendships = Friendship.objects.filter(from_user=pk).order_by('-created_at')
        serializer = FollowingSerializer(friendships, many=True)

        # normally, response has to be a hash instead of a list
        return Response({'followings': serializer.data})

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def follow(self, request, pk):
        # api/friendships/1/follow
        if Friendship.objects.filter(
                from_user_id=request.user.id,
                to_user_id=pk
        ).exists():
            return Response({
                'success': True,
                'duplicate': True,
            }, status=status.HTTP_201_CREATED)

        serializer = FriendshipCreateSerializer(
            data={
                'from_user_id':request.user.id,
                'to_user_id':pk,
            }
        )
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        # normally, response has to be a hash instead of a list
        return Response({'friendship': serializer.data}, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk):
        # api/friendships/1/unfollow
        if int(pk) == request.user.id:
            return Response({
                'success': False,
                'errors': 'you cannot unfollow yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        deleted,_ = Friendship.objects.filter(
            from_user_id = request.user.id,
            to_user_id = pk
        ).delete()

        # normally, response has to be a hash instead of a list
        return Response({'deleted': deleted})

    def list(self,request):
        return Response({'response':'friendship home page'})

