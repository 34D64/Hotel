from django.db import models

class Room(models.Model):
    ROOM_TYPES = [
        ('luxury', 'لوکس'),
        ('economic', 'اقتصادی'),
        ('suite', 'سوییت خانوادگی'),
    ]
    name = models.CharField("نام اتاق", max_length=100)
    room_type = models.CharField("نوع اتاق", max_length=20, choices=ROOM_TYPES)
    price = models.PositiveIntegerField("قیمت (تومان)")
    beds = models.FloatField("تعداد تخت")
    image = models.ImageField("تصویر", upload_to='rooms/')

    def __str__(self):
        return self.name

class Booking(models.Model):
    name = models.CharField("نام رزرو کننده", max_length=100)
    room = models.ForeignKey(Room, verbose_name="اتاق", on_delete=models.CASCADE)
    checkin = models.DateField("تاریخ ورود")
    checkout = models.DateField("تاریخ خروج")
    created = models.DateTimeField("زمان ثبت رزرو", auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    authority = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} → {self.room.name}"
