from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'room', 'checkin', 'checkout']
        widgets = {
            'checkin': forms.DateInput(attrs={'type': 'date'}),
            'checkout': forms.DateInput(attrs={'type': 'date'}),
        }
