from django.shortcuts import render, redirect
from .models import Room
from .forms import BookingForm

def index(request):
    rooms = Room.objects.all()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Make sure your urls.py has name='index'
        else:
            print(form.errors)  # Debug: check form errors in console
    else:
        form = BookingForm()

    return render(request, 'home/index.html', {
        'rooms': rooms,
        'form': form
    })
