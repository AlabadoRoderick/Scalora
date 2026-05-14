from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control scalora-input', 'placeholder': 'Email Address'
    }))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control scalora-input', 'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control scalora-input', 'placeholder': 'Last Name'
    }))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control scalora-input', 'placeholder': 'Phone Number (optional)'
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control scalora-input', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control scalora-input', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control scalora-input', 'placeholder': 'Confirm Password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role='client',
                phone=self.cleaned_data.get('phone', '')
            )
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control scalora-input', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control scalora-input', 'placeholder': 'Password'})


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control scalora-input'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control scalora-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control scalora-input'}))

    class Meta:
        model = UserProfile
        fields = ['phone', 'bio', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control scalora-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-control scalora-input', 'rows': 4}),
            'avatar': forms.FileInput(attrs={'class': 'form-control scalora-input'}),
        }
