# views.py
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from .models import Room, Booking
from .forms import BookingForm

def index(request):
    today = timezone.localdate()
    form = BookingForm(request.POST or None)

    # Get dates from GET params for filtering available rooms
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')

    # Default to today + 1 day if not provided
    if not checkin or not checkout:
        checkin = today
        checkout = today.replace(day=today.day + 1)  # basic 1-day default
    else:
        # Convert to date objects
        from datetime import datetime
        checkin = datetime.strptime(checkin, "%Y-%m-%d").date()
        checkout = datetime.strptime(checkout, "%Y-%m-%d").date()

    # Handle booking form submission
    if request.method == 'POST' and form.is_valid():
        f_checkin = form.cleaned_data['checkin']
        f_checkout = form.cleaned_data['checkout']
        room = form.cleaned_data['room']

        # Date validation
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
                booking.is_paid = True  # no payment gateway in this example
                booking.save()
                return HttpResponse("رزرو شما با موفقیت ثبت شد!")

    # Available rooms based on selected date range
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


def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'home/booking_detail.html', {'booking': booking})
