from django.contrib import admin
from .models import Room, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_type', 'price', 'beds')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'room', 'checkin', 'checkout', 'created')
