from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from inbox.services import NotificationService
from likes.api.serializers import LikeCreateSerializer, LikeSerializer, LikeCancelSerializer
from likes.models import Like
from utils.decorators import required_params


class LikeViewSet(viewsets.GenericViewSet):
    serializer_class = LikeCreateSerializer
    queryset = Like.objects.all()

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @required_params(request_attr='data', params=['content_type', 'object_id'])
    def create(self, request, *args, **kwargs):
        """
        overload create method
        """
        serializer = LikeCreateSerializer(
            data=request.data,
            context={'request': request},
        )
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        like = serializer.save()
        NotificationService.send_like_notification(like)
        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    @required_params(request_attr='data', params=['content_type', 'object_id'])
    def cancel(self, request, *args, **kwargs):
        serializer = LikeCancelSerializer(
            data=request.data,
            context={'request': request},
        )
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.cancel()
        return Response({'success': 'True'}, status=status.HTTP_200_OK)
