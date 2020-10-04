import re

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields =['message', 'photo', 'tag_set', 'is_public']
    
    # Form 함수내에서 특정 DB(여기서는 message)에 대해서 유효성 검사를 수행하는 함수
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message:
            message = re.sub(r'[a-zA-Z]+', '', message)
        return message