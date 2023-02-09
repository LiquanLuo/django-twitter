from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from newsfeeds.api.serializers import NewsfeedSerializer
from newsfeeds.models import Newsfeed


class NewsfeedViewSet(viewsets.GenericViewSet):
    queryset = Newsfeed.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """

        permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        """
        overload list method
        """

        newsfeeds = Newsfeed.objects.filter(user = request.user).order_by('-created_at')
        serializer = NewsfeedSerializer(newsfeeds,
                                        context={'request': request},
                                        many = True)

        # normally, response has to be a hash instead of a list
        return Response({'newsfeeds': serializer.data})




