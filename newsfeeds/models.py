from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from tweets.models import Tweet


class NewsFeed(models.Model):
    # 注意这个 user 不是存储谁发了这条 tweet，而是谁可以看到这条 tweet
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.SET_NULL, null=True)
    # 在创建表的时候不指定数据类型，而是在存储数据的时候才动态指定数据类型
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 指定一些配置信息
        index_together = (('user', 'created_at'),)
        unique_together = (('user', 'tweet'),)
        # 规定排序的方式，但是不改变表的存储结构
        ordering = ('user', '-created_at',)

    def __str__(self):
        return f'{self.created_at} inbox of {self.user}: {self.tweet}'
