from django.db import models
from django.conf import settings

class AvailabilitySlot(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'doctor'}
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor.username} - {self.date} {self.start_time} to {self.end_time}"

class Booking(models.Model):
    slot = models.OneToOneField(
        AvailabilitySlot,
        on_delete=models.CASCADE
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'}
    )
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} booked {self.slot}"
