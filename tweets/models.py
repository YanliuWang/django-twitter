from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from likes.models import Like
from utils.time_helpers import utc_now

# Create your models here.
class Tweet(models.Model):
    # 表示发帖人，为当前登录的 user
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (('user', 'created_at'),)
        # 查询数据的时候先按照 user_id 生序排列
        # 再按照 created_time 降序排列
        ordering = ('user', '-created_at')


    @property
    def hours_to_now(self):
        # datetime.now 不带时区信息，需要增加上 utc 的时区信息
        # 知道这个推文距离现在发表了多少个小时
        return (utc_now() - self.created_at).seconds // 3600

    def __str__(self):
        # 这里是你执行 print(tweet instance) 的时候会显示的内容
        return f'{self.created_at} {self.user}: {self.content}'

    @property
    def like_set(self):
        return Like.objects.filter(
            content_type=ContentType.objects.get_for_model(Tweet),
            object_id=self.id,
        ).order_by('-created_at')