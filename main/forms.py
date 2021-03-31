from django import forms
from django.contrib.auth.models import User
from .models import Comment
from django.forms import Textarea
from .models import UserProfile


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} не найден в системе!')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['phone_number'].label = 'Номер телефона'
        self.fields['first_name'].label = 'Ваше имя'
        self.fields['last_name'].label = 'Ваша фамилия'
        self.fields['email'].label = "Электронная почта"
        self.fields['avatar'].label = "Фото"
        self.fields['password'].label = "Пароль"

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Данный почтовый адресс уже зарегестрирован в системе')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Имя {username} занято')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'email', 'phone_number',
                  'avatar']


class ProfileEditFormUser(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['first_name'].label = 'Ваше имя'
        self.fields['last_name'].label = 'Ваша фамилия'
        self.fields['email'].label = "Электронная почта"
        self.fields['password'].label = "Пароль"

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', ]


class ProfileEditFormUserProfile(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].label = 'Номер телефона'
        self.fields['avatar'].label = "Фото"

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'avatar']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': Textarea(attrs={'rows': 3, 'cols': 30}),
        }
