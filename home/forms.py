import jdatetime
from django import forms
from .models import Booking

def persian_to_english_digits(persian_str):
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    translation_table = str.maketrans(''.join(persian_digits), ''.join(english_digits))
    return persian_str.translate(translation_table)

class BookingForm(forms.ModelForm):
    checkin = forms.CharField(
        label='تاریخ ورود',
        widget=forms.TextInput(attrs={'id': 'id_checkin', 'autocomplete': 'off'})
    )
    checkout = forms.CharField(
        label='تاریخ خروج',
        widget=forms.TextInput(attrs={'id': 'id_checkout', 'autocomplete': 'off'})
    )

    class Meta:
        model = Booking
        fields = ['name', 'room', 'checkin', 'checkout']
        labels = {
            'name': 'نام رزرو کننده',
            'room': 'اتاق',
        }

    def clean_checkin(self):
        jalali_date_str = self.cleaned_data['checkin']
        jalali_date_str = persian_to_english_digits(jalali_date_str)
        try:
            jd = jdatetime.datetime.strptime(jalali_date_str, "%Y/%m/%d")
            return jd.togregorian().date()
        except Exception:
            raise forms.ValidationError("تاریخ ورود نامعتبر است.")

    def clean_checkout(self):
        jalali_date_str = self.cleaned_data['checkout']
        jalali_date_str = persian_to_english_digits(jalali_date_str)
        try:
            jd = jdatetime.datetime.strptime(jalali_date_str, "%Y/%m/%d")
            return jd.togregorian().date()
        except Exception:
            raise forms.ValidationError("تاریخ خروج نامعتبر است.")
