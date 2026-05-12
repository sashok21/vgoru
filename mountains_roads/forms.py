from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .mixins import CssWidgetMixin
from .models import RouteReview, UserProfile


class RouteReviewForm(CssWidgetMixin, forms.ModelForm):
    class Meta:
        model = RouteReview
        fields = ['rating', 'title', 'text']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'title': forms.TextInput(attrs={'placeholder': 'Заголовок відгуку'}),
            'text': forms.Textarea(attrs={'placeholder': 'Поділіться враженням...', 'rows': 4}),
        }


class UserRegistrationForm(CssWidgetMixin, UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "Ім'я"}),
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Прізвище'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "Ім'я користувача"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Пароль'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Повторіть пароль'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Користувач з такою адресою вже існує.')
        return email


class UserProfileForm(CssWidgetMixin, forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Розкажіть про себе...', 'rows': 4}),
            'avatar': forms.FileInput(attrs={'accept': 'image/*'}),
        }
