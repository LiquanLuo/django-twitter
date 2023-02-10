from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from comments.api.serializers import CommentSerializer, CommentCreateSerializer, CommentUpdateSerializer
from comments.models import Comment
from comments.api.permissions import IsObjectOwner
from inbox.services import NotificationService

from utils.decorators import required_params


class CommentViewSet(viewsets.GenericViewSet):
    serializer_class = CommentCreateSerializer
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('tweet_id',)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [permissions.AllowAny]
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update','destroy']:
            permission_classes = [permissions.IsAuthenticated, IsObjectOwner,]


        return [permission() for permission in permission_classes]

    # POST   /api/comments/            -> create
    # GET    /api/comments/?tweet_id=1 -> list
    # GET    /api/comments/1/          -> retrieve
    # DELETE /api/comments/1/          -> destroy
    # PATCH  /api/comments/1/          -> partial_update
    # PUT    /api/comments/1/          -> update


    def create(self, request, *args, **kwargs):
        """
        overload create method
        """
        comment_data = {
            'user_id' : request.user.id,
            'tweet_id' : request.data.get('tweet_id'),
            'content': request.data.get('content'),
        }
        serializer = CommentCreateSerializer(data=comment_data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        comment = serializer.save()
        NotificationService.send_comment_notification(comment)
        return Response(CommentSerializer(comment, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        overload update method
        """
        serializer = CommentUpdateSerializer(
            instance = self.get_object(),
            data=request.data,
        )
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        comment = serializer.save()
        return Response(CommentSerializer(comment, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)

    @required_params(request_attr='query_params', params=['tweet_id'])
    def list(self, request):
        """
        overload list method, do not allow request without tweet_id
        """
        queryset = self.filter_queryset(
            self.get_queryset()
        ).order_by('created_at')

        serializer = CommentSerializer(queryset, context={'request': request}, many = True)

        # normally, response has to be a hash instead of a list
        return Response({'comments': serializer.data})
