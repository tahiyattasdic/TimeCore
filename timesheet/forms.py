from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    # We are adding a new field for email
    email = forms.EmailField(
        required=True,
        help_text='A valid email address is required.'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # Add 'email' to the list of fields to be displayed and saved
        fields = UserCreationForm.Meta.fields + ('email',)