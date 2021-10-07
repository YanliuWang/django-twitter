from django.contrib.auth.models import User
from rest_framework import serializers, exceptions

# 可以验证用户的输入是否符合要求
# 规定数据输出的格式
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class LoginSerializer(serializers.Serializer):
    # 检测这两项是否有输入
    # required 默认为 true 要有数据
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        # user does not exist
        if not User.objects.filter(username=data['username'].lower()).exists():
            raise exceptions.ValidationError({
                'username': 'This user does not exist.'
            })
        return data


# 继承于 ModelSerializer 表示可以创建一个数据
class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, min_length=6)
    password = serializers.CharField(max_length=20, min_length=6)
    email = serializers.EmailField()

    class Meta:
        model = User
        # 规范数据的格式
        fields = ('username', 'email', 'password')

    # will be called when is_valid() is called
    def validate(self, data):
        # 大小写不敏感
        if User.objects.filter(username=data['username'].lower()).exists():
            raise exceptions.ValidationError({
                'username': 'This username has been occupied.'
            })

        if User.objects.filter(email=data['email'].lower()).exists():
            raise exceptions.ValidationError({
                'email': 'This email has been occupied.'
            })
        return data

    def create(self, validated_data):
        # 用小写存起来
        username = validated_data['username'].lower()
        email = validated_data['email'].lower()
        password = validated_data['password']

        # 创建 user 使用 create_user
        # 把 password 明文转换成密文
        # 把 username 和 email 进行 normalize
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        return user



