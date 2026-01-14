from django.urls import path
from .views import (
    doctor_availability,
    patient_slots,
    book_slot,
    doctor_bookings
)

urlpatterns = [
    path('doctor/availability/', doctor_availability, name='doctor_availability'),
    path('doctor/bookings/', doctor_bookings, name='doctor_bookings'),
    path('patient/slots/', patient_slots, name='patient_slots'),
    path('patient/book/<int:slot_id>/', book_slot, name='book_slot'),
]
