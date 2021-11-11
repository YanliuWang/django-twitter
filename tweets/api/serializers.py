from accounts.api.serializers import UserSerializer
from rest_framework import serializers
from tweets.models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Tweet
        # 请求成功之后返回这些数据给前端
        fields = ('id', 'user', 'created_at', 'content')


class TweetCreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(min_length=6, max_length=140)

    class Meta:
        model = Tweet
        fields = ('content',)

    # 重载 create 方法
    # 调用序列化实例的 save() 时，自动调用
    def create(self, validated_data):
        # 获取当前登录的用户，设为发帖人
        user = self.context['request'].user
        content = validated_data['content']
        tweet = Tweet.objects.create(user=user, content=content)
        return tweet
