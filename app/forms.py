from django import forms
from django.contrib.auth.models import User
from app import models
from app.models import Answer, Question, Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(self.cleaned_data.get('username')) > 10:
            raise forms.ValidationError('Username too long')
        return username


class SignupForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, required=True)
    avatar = forms.ImageField(required=False)

    def clean(self):
        password = self.cleaned_data['password']
        password_confirmation = self.cleaned_data['password_confirmation']
        if len(password) < 8:
            raise forms.ValidationError('Password is too short')
        if password != password_confirmation:
            raise forms.ValidationError("Passwords don't match")

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email already exists')
        return email

    def save(self):
        avatar = self.cleaned_data['avatar']
        user = User.objects.create_user(username=self.cleaned_data['username'],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password'])
        models.Profile.objects.create(user=user, avatar=avatar)
        return user



class AnswerForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea,
        label='',
    )

    class Meta:
        model = Answer
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) == 0:
            raise forms.ValidationError('Answer too short')
        if len(content) > 512:
            raise forms.ValidationError('Answer too long')
        return content

class AskQuestion(forms.ModelForm):
    title = forms.CharField(
        max_length=128,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Title'}),
    )

    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Content'}),
        max_length=512,
        label='',
    )

    tags = forms.CharField(
        required=True,
        help_text="Введите теги через пробел, например: django python",
        widget=forms.TextInput(attrs={'placeholder': 'Tags'}),
        label='',
    )

    class Meta:
        model  = Question
        fields = ['title', 'content', 'tags']

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError('Title cannot be empty')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError('Content cannot be empty')
        return content

    def clean_tags(self):
        raw = self.cleaned_data.get('tags', '').strip()
        if not raw:
            raise forms.ValidationError('Please enter at least one tag')
        names = {t.strip() for t in raw.split() if t.strip()}
        if not names:
            raise forms.ValidationError('Please enter valid tag names')
        return list(names)


class SettingsForm(forms.ModelForm):
    username = forms.CharField(label='Login', disabled=True, required=False)
    email    = forms.EmailField(label='Email', disabled=True, required=False)
    avatar   = forms.ImageField(label='New Avatar', required=False)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': self.instance.user.username,
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': self.instance.user.email,
        })




