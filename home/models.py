from django.db import models

class Room(models.Model):
    ROOM_TYPES = [
        ('luxury', 'لوکس'),
        ('economic', 'اقتصادی'),
        ('suite', 'سوییت خانوادگی'),
    ]

    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.PositiveIntegerField()
    beds = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='rooms/')

    def __str__(self):
        return self.name

class Booking(models.Model):
    name = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    checkin = models.DateField()
    checkout = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} → {self.room.name}"
