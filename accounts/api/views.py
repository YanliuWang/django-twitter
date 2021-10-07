from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from accounts.api.serializers import UserSerializer



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # 每一次操作都必须进行登录检测
    permission_classes = [permissions.IsAuthenticated]