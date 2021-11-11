from django.contrib import admin
from comments.models import Comment

# 定义在 admin 界面看到模型的格式
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('tweet', 'user', 'content', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
