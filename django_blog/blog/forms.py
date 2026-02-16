from .models import Comment
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from taggit.forms import TagWidget


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']



from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # include tags
        widgets = {
            'tags': TagWidget(),               # <-- specify TagWidget
        }





class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']


