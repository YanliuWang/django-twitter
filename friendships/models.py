from django.db import models
from django.contrib.auth.models import User


class Friendship(models.Model):
    # related_name 是起一个别名

    # user 关注的人
    # 表示发起关注的人
    from_user = models.ForeignKey(
        User,
        # set the record to null instead of deletion
        on_delete=models.SET_NULL,
        null=True,
        related_name='following_friendship_set',
    )

    # 关注 user 的人
    # 表示被关注的人
    to_user = models.ForeignKey(
        User,
        # set the record to null instead of deletion
        on_delete=models.SET_NULL,
        null=True,
        related_name='follower_friendship_set',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (
            # 获取我关注的所有人，按照关注时间排序
            ('from_user_id', 'created_at'),
            # 获得关注我的所有人，按照关注时间排序
            ('to_user_id', 'created_at'),
        )
        # 不能同时关注一个人两次
        unique_together = (('from_user_id', 'to_user_id'),)

    def __str__(self):
        return '{} followed {}'.format(self.from_user_id, self.to_user_id)
