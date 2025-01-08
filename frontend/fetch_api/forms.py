from django import forms
from .models import Customer

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'تلفن'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
