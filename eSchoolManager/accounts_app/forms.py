from django.contrib.auth import get_user_model
from django.contrib.auth.forms import BaseUserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django import forms

from eSchoolManager.accounts_app.models import SchoolUser

UserModel = get_user_model()


class UserCreationForm(BaseUserCreationForm):
    def clean_email(self):
        """Reject usernames that differ only in case."""
        email = self.cleaned_data.get("email")
        if (
                email
                and self._meta.model.objects.filter(email__iexact=email).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "email": self.instance.unique_error_message(
                            self._meta.model, ["email"]
                        )
                    }
                )
            )
        else:
            return email


class SchoolUserRegistrationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


class SchoolUserEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            })
        }


class SchoolUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control',
                                                     'type': 'email'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
