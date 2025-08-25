from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
from .models import Room, Booking
from .forms import BookingForm

def index(request):
    today = timezone.localdate()
    form = BookingForm(request.POST or None)

    # Get dates
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')

    from datetime import datetime, timedelta
    if not checkin or not checkout:
        checkin = today
        checkout = today + timedelta(days=1)
    else:
        checkin = datetime.strptime(checkin, "%Y-%m-%d").date()
        checkout = datetime.strptime(checkout, "%Y-%m-%d").date()

    # booking submit
    if request.method == 'POST' and form.is_valid():
        f_checkin = form.cleaned_data['checkin']
        f_checkout = form.cleaned_data['checkout']
        room = form.cleaned_data['room']

        if f_checkin < today or f_checkout <= f_checkin:
            form.add_error('checkin', 'تاریخ ورود نامعتبر یا کوچکتر از امروز است')
            form.add_error('checkout', 'تاریخ خروج باید بزرگتر از ورود باشد')
        else:
            overlap = Booking.objects.filter(
                room=room,
                checkin__lt=f_checkout,
                checkout__gt=f_checkin,
                is_paid=True
            ).exists()

            if overlap:
                form.add_error('room', 'اتاق در این بازه زمانی رزرو شده است')
            else:
                booking = form.save(commit=False)
                booking.is_paid = False   # not paid yet
                booking.save()
                # redirect to fake payment page
                return redirect('fake_payment', booking_id=booking.id)

    rooms = Room.objects.exclude(
        id__in=Booking.objects.filter(
            is_paid=True,
            checkin__lt=checkout,
            checkout__gt=checkin
        ).values_list('room_id', flat=True)
    )

    return render(request, 'home/index.html', {
        'form': form,
        'rooms': rooms,
        'checkin': checkin,
        'checkout': checkout
    })


def fake_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    # calc 70% of price
    pay_amount = int(booking.room.price * 0.7)

    if request.method == 'POST':
        booking.is_paid = True
        booking.save()
        return redirect('index')  # back to home

    return render(request, 'home/fake_payment.html', {
        'booking': booking,
        'pay_amount': pay_amount
    })
