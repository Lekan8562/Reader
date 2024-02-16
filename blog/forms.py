from .models import Comment,Post,Reply,Subsciber
from django import forms
from users.models import CustomUser
from users.models import CustomUser
from django.contrib.auth import password_validation
from froala_editor.fields import FroalaField


class SubsciberForm(forms.ModelForm):
    class Meta:
        model = Subsciber
        fields = ['email']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','body']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['name','email','body']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','images','body','tag','status']
        
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False,widget=forms.Textarea)



class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    avatar = forms.ImageField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    bio = forms.CharField(widget=forms.Textarea)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)