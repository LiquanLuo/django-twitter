from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from newsfeeds.services import NewsFeedService
from tweets.models import Tweet
from tweets.api.serializers import (
    TweetSerializer,
    TweetCreateSerializer,
    TweetSerializerWithComments,
)
from utils.decorators import required_params


class TweetViewSet(viewsets.GenericViewSet):
    serializer_class = TweetCreateSerializer
    queryset = Tweet.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in  ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @required_params(params=['user_id'])
    def list(self, request):
        """
        overload list method, do not allow request without user_id
        """

        user_id = self.request.query_params.get("user_id")

        # this query will be translated to
        # select * from twitter_tweets
        # where user_id = xxx
        # order by created_at desc
        # which will use the compound index of user and created_at
        # only index user is not sufficient
        tweets = Tweet.objects.filter(user_id = user_id).order_by('-created_at')
        serializer = TweetSerializer(tweets,
                                     context={'request': request},
                                     many = True
                                     )

        # normally, response has to be a hash instead of a list
        return Response({'tweets': serializer.data})

    def create(self, request, *args, **kwargs):
        """
        overload create method
        """
        serializer = TweetCreateSerializer(
            data=request.data,
            context={'request': request},
        )
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        tweet = serializer.save()
        NewsFeedService.fanout_to_followers(tweet)
        return Response(TweetSerializer(tweet, context={'request': request},).data,
                        status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        tweet = self.get_object()
        return Response(TweetSerializerWithComments(tweet, context={'request': request},).data,
                        status=status.HTTP_200_OK)


