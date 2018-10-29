from django.contrib.auth.models import AbstractUser
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models


class User(AbstractUser):
    img_profile = models.ImageField(
        '프로필 이미지',
        upload_to='user',
        blank=True,
    )
    site = models.URLField(
        '사이트',
        max_length=150,
        blank=True,
    )
    introduce = models.TextField('소개', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    @property
    def img_profile_url(self):
        # 자신의 img_profile필드에 내용이 있다면
        # 해당 파일로 접근할 수 있는 url을 리턴
        if self.img_profile:
            return self.img_profile.url
        # 없다면 static폴더에서 뒷 경로 파일의 url을 리턴
        return static('images/blank_user.png')

    def like_post_toggle(self, post):
        # 자신에게 연결된 PostLike중, post값이 매개변수의 post인 PostLike가 있다면 가져오고, 없으면 생성
        postlike, postlike_created = self.postlike_set.get_or_create(post=post)
        # 생성되었다면 없다가 생겼다는 말이므로(새로 좋아요를 누름) 따로 처리 필요없음
        # 생성되지 않았다면 이미 있었다는 말이므로 toggle처리를 위해 삭제
        if not postlike_created:
            postlike.delete()