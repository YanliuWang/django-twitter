from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.api.serializers import (
    UserSerializer,
    LoginSerializer,
    SignupSerializer,
)
from django.contrib.auth import (
    logout as django_logout,
    login as django_login,
    authenticate as django_authenticate,
)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    ModelViewSet 可以增删查改操作
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccountViewSet(viewsets.ViewSet):
    serializer_class = SignupSerializer

    # 主目录下面的文件是可以自定义成一个动作
    # 严格的 REST 风格只能用 http 的增删查改完成某个动作
    # detail=false 指的是定义在整个目录上的动作，不需要在前面加上数字
    @action(methods=['GET'], detail=False)
    def login_status(self, request):
        data = {'has_logged_in': request.user.is_authenticated}
        # if login in
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
        return Response(data)

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        django_logout(request)
        return Response({'success': True})

    @action(methods=['POST'], detail=False)
    def login(self, request):
        # get username and password from request
        # POST -> request.data
        serializer = LoginSerializer(data=request.data)

        # input data is not valid
        if not serializer.is_valid():
            # status is default set as 200
            return Response({
                "success": False,
                "message": "Please check input",
                "errors": serializer.errors
            }, status=400)

        # validation ok
        # username and password are preprocessed
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # use print to get sql
        # queryset = User.objects.filter(username=username)
        # print(queryset)

        # user does not exist
        if not User.objects.filter(username=username).exists():
            return Response({
                "success": False,
                "message": "User does not exist.",
            }, status=400)

        # authentication test
        user = django_authenticate(username=username, password=password)
        # authentication failed
        if not user or user.is_anonymous:
            return Response({
                "success": False,
                "message": "username and password does not match.",
            }, status=400)

        # authentication succeed
        django_login(request, user)
        return Response({
            "success": True,
            "user": UserSerializer(instance=user).data
        })

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        """
        使用 username, email, password 进行注册
        """
        # 不太优雅的写法
        # username = request.data.get('username')
        # if not username:
        #     return Response("username required", status=400)
        # password = request.data.get('password')
        # if not password:
        #     return Response("password required", status=400)
        # if User.objects.filter(username=username).exists():
        #     return Response("password required", status=400)
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Please check input",
                'errors': serializer.errors,
            }, status=400)

        user = serializer.save()
        django_login(request, user)

        return Response({
            'success': True,
            'user': UserSerializer(user).data,
        }, status=201)






