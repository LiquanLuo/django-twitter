from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from inbox.api.serializers import NotificationSerializer, NotificationUpdateSerializer
from utils.decorators import required_params


class NotificationViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('unread',)

    def get_queryset(self):
        return self.request.user.notifications.all()

    @action(methods=['GET'], detail=False, url_path='unread-count')
    def unread_count(self, request, *args, **kwargs):
        unread_count = self.get_queryset().filter(unread=True).count()
        return Response({'unread_count': unread_count}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, url_path='mark-all-as-read')
    def mark_all_as_read(self, request, *args, **kwargs):
        updated_count = self.get_queryset().filter(unread=True).update(unread=False)
        return Response({'updated_count': updated_count}, status=status.HTTP_200_OK)

    @required_params(request_attr='data', params=['unread'])
    def update(self, request, *args, **kwargs):
        serializer = NotificationUpdateSerializer(
            instance = self.get_object(),
            data=request.data
        )
        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'errors' : serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        notification = serializer.save()
        return Response(NotificationSerializer(notification).data,
                        status=status.HTTP_200_OK)
