from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinLengthValidator

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(validators=[MinLengthValidator(5)]) # 최소 5글자
    photo = models.ImageField(blank=True, upload_to = 'instagram/post/%Y%m%d') # upload_to를 사용 안하면 media 폴더 한개 안에 너무 많은 이미지 파일이 쌓일 수도 있음. 
                                                                            # 옆과 같이 설정하면 media 폴더 안에 하위 폴더를 만들어서 여기에 따로 모아줌. 
                                                                            # 이렇게 하면 검색속도도 빨라지고 좋음
                                                                            # %Y%m%d로 그날의 날짜에 맞게 폴더 명을 새로 생성 %H%M%S도 있음
                                                                            # upload_to에서 함수 지정을 통해서 업로드 될 파일의 이름을 임의로 변경해서 올릴수도 있음
    is_public = models.BooleanField(default=False, verbose_name = '공개여부')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag_set = models.ManyToManyField('Tag', blank=True) 
    # 여기서 지정하거나 밑에서 MTM을 지정하면된다. 
    # 주의점! Tag 클래스의 경우 코드 순서상 아직 읽어오지 않았으므로 그냥 Tag라고 쓰면 안되고 'Tag' 처럼 문자 형태로 써줘야한다

    # admin에 출력될때 어떤 식으로 표현할지 지정
    def __str__(self):
        return f'{self.message} ({self.id})'

    # default 정렬기능
    class Meta:
        ordering = ['-id']

    # 이건 admin.py에 구현해도 상관 없다
    def message_length(self):
        return f"{len(self.message)} 글자"
    message_length.short_description = '메세지 글자수'

    # url 계산을 위해서 만들어줌
    def get_absolute_url(self):
        return reverse('instagram:post_detail', args=[self.pk])



class Comment(models.Model):
    post = models.ForeignKey('instagram.Post', on_delete=models.CASCADE, limit_choices_to={'is_public':True})    
    # Post 클래스와 1:n의 관계, 다른 앱의 Model 클래스를 위에서 import해서 쓰면 여기서 1:n 관계를 지정해줄수 있다
    # on_delete=models.CASCADE를 사용해서 부모격의 글이 지워지면 그 밑에 달린 comment도 다같이 지워버리는 기능을 추가
    # limit_choices_to를 사용해서 특정 조건일때만 comment를 달수있게 하기도 한다
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tag(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    # post_set = models.ManyToManyField(Post, blank=True)   # 여기서 MTM을 지정하거나 위에서 지정하거나 둘중 하나만 하면 된다

    def __str__(self):
        return self.name