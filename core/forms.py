from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Item
from django.forms.widgets import SelectDateWidget
import datetime

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create password',
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'password']
        labels = {
            'username': 'Register Number',
            'first_name': 'Student Name',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'e.g. 21CS001',
                'class': 'form-control'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'e.g. John Doe',
                'class': 'form-control'
            }),
        }

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Register Number'
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter Register Number',
            'class': 'form-control'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Enter Password',
            'class': 'form-control'
        })

class ItemForm(forms.ModelForm):
    current_year = datetime.date.today().year
    YEAR_CHOICES = [r for r in range(current_year - 5, current_year + 1)]

    event_date = forms.DateField(
        label="Date Lost/Found",
        widget=SelectDateWidget(
            years=YEAR_CHOICES,
            attrs={'class': 'date-select'}
        )
    )

    class Meta:
        model = Item
        fields = [
            'title',
            'description',
            'category',
            'location',
            'report_type',
            'event_date',
            'image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. Black leather wallet',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe the item details (brand, color, contents)...',
                'rows': 4,
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'report_type': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }