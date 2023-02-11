from django.contrib.auth.models import User, Group
from django.contrib.auth import (
    authenticate as django_authenticate,
    login as django_login,
    logout as django_logout,
)
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.api.serializers import (
    UserSerializer,
    LoginSerializer,
    SignUpSerializer
)


class AccountViewSet(viewsets.ViewSet):
    serializer_class = SignUpSerializer

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        serializer = SignUpSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=400)

        user = serializer.save()

        # Create UserProfile
        user.profile

        django_login(request, user)
        return Response({
            'success': True,
            'user': UserSerializer(instance=user).data
        })


    @action(methods=['GET'], detail=False)
    def login_status(self, request):
        data = {
            'login': request.user.is_authenticated,
            'ip': request.META['REMOTE_ADDR']
        }
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
        return Response(data)

    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input",
                "errors": serializer.errors,
            }, status=400)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = django_authenticate(username = username, password = password)
        if not user or user.is_anonymous:
            return Response({
                "success": False,
                "message": "username and password does not match"
            }, status=400)
        django_login(request, user)
        return Response({"success": True,
                         "user": UserSerializer(instance=user).data,
                         })

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        django_logout(request)
        data = {'success': True}
        return Response(data)



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
