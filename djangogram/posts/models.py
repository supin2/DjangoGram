from django.db import models
from django.db.models.fields import related
from djangogram.users import models as user_model

# Create your models here.
class TimeStamedModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    # 아래 옵션이 추가되면 TimeStamedModel은 단독으로 테이블 생성이 안됨
    class Meta: 
        abstract = True

# 사진 저장
class Post(TimeStamedModel):
    author = models.ForeignKey( 
        user_model.User, # User 모델의 User Table을 가리킴(외래키)
        null=True, 
        on_delete=models.CASCADE, 
        related_name='post_author'
    ) 
    image = models.ImageField(blank=False)
    caption = models.TextField(blank=False)
    image_likes = models.ManyToManyField(user_model.User, related_name='post_image_likes')

# 댓글 관리
class Comment(TimeStamedModel):
    author = models.ForeignKey(
        user_model.User,  # User 모델의 User Table을 가리킴(외래키)
        null=True, 
        on_delete=models.CASCADE, 
        related_name='comment_author'
    )
    posts = models.ForeignKey(
        Post,  # 위의 Post를 가리킴(외래키)
        null=True,
        on_delete=models.CASCADE,
        related_name='comment_post'
    )
    contents = models.TextField(blank=True)