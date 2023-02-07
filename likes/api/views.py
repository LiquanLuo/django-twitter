from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from likes.api.serializers import LikeCreateSerializer, LikeSerializer
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
        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)