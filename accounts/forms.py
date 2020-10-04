from django import forms
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'zipcode']

# 여기서 로그인하기 위한 조건을 설정해줄 수 있다
class LoginForm(AuthenticationForm):
    answer = forms.IntegerField(help_text='3 + 3 = ?')
    def clean_answer(self):
        answer = self.cleaned_data.get('answer')
        if answer != 6:
            raise forms.ValidationError('땡~!')
        return answer


