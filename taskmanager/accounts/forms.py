from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class AssignAdminForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(role='User'),
        label="Select User",
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg rounded-3 shadow-sm'
        })
    )

    admin = forms.ModelChoiceField(
        queryset=User.objects.filter(role='Admin'),
        label="Select Admin",
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg rounded-3 shadow-sm'
        })
    )
