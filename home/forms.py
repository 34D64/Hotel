from django import forms
from django.utils import timezone
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'codemeli', 'room', 'checkin', 'checkout']  # 👈 کدملی اضافه شد
        labels = {
            'name': 'نام رزرو کننده',
            'codemeli': 'کدملی',
            'room': 'اتاق',
            'checkin': 'تاریخ ورود',
            'checkout': 'تاریخ خروج',
        }
        widgets = {
            'checkin': forms.DateInput(attrs={'type': 'date'}),
            'checkout': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.localdate().isoformat()
        self.fields['checkin'].widget.attrs['min'] = today
        self.fields['checkout'].widget.attrs['min'] = today

    def clean(self):
        cleaned_data = super().clean()
        checkin = cleaned_data.get('checkin')
        checkout = cleaned_data.get('checkout')
        codemeli = cleaned_data.get('codemeli')
        today = timezone.localdate()

        # validate dates
        if checkin and checkin < today:
            self.add_error('checkin', 'تاریخ ورود نمی‌تواند به گذشته باشد.')

        if checkin and checkout and checkout <= checkin:
            self.add_error('checkout', 'تاریخ خروج باید بعد از تاریخ ورود باشد.')

        # validate codemeli (should be exactly 10 digits)
        if codemeli and (not codemeli.isdigit() or len(codemeli) != 10):
            self.add_error('codemeli', 'کدملی باید دقیقا ۱۰ رقم عددی باشد.')
