from django.contrib.auth import (authenticate, get_user_model, login, logout, )
from django import forms
from .models import User

#User = get_user_model()

class UserLoginForm(forms.Form):
    #username = forms.CharField(max_length=128) #technically just email for normal users
    email = forms.EmailField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)
    #firstName = models.CharField(max_length=32)
    #lastName = models.CharField(max_length=32)
    #phoneNumber = models.CharField(max_length=11)
    #nickname = models.CharField(max_length=128)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label="User/Email")
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'name',
            'phoneNum',

        ]


