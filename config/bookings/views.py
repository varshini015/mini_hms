from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AvailabilityForm
from .models import AvailabilitySlot,Booking



@login_required
def doctor_availability(request):
    if request.user.role != 'doctor':
        return redirect('dashboard')

    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.doctor = request.user
            slot.save()
            return redirect('doctor_availability')
    else:
        form = AvailabilityForm()

    slots = AvailabilitySlot.objects.filter(doctor=request.user)

    return render(
        request,
        'bookings/doctor_availability.html',
        {'form': form, 'slots': slots}
    )

@login_required
def patient_slots(request):
    if request.user.role != 'patient':
        return redirect('dashboard')

    slots = AvailabilitySlot.objects.filter(is_booked=False)

    return render(
        request,
        'bookings/patient_slots.html',
        {'slots': slots}
    )

from django.db import transaction
from datetime import datetime
from .google_calendar import create_calendar_event

@login_required
def book_slot(request, slot_id):
    if request.user.role != 'patient':
        return redirect('dashboard')

    with transaction.atomic():
        slot = AvailabilitySlot.objects.select_for_update().get(id=slot_id)

        if slot.is_booked:
            return redirect('patient_slots')

        # 1️⃣ Create booking
        Booking.objects.create(
            slot=slot,
            patient=request.user
        )

        # 2️⃣ Mark slot as booked
        slot.is_booked = True
        slot.save()

        # 3️⃣ GOOGLE CALENDAR INTEGRATION (ADD HERE 👇)
        start_dt = datetime.combine(slot.date, slot.start_time)
        end_dt = datetime.combine(slot.date, slot.end_time)

        # Patient calendar
        create_calendar_event(
            request.user,
            f"Appointment with Dr. {slot.doctor.username}",
            start_dt,
            end_dt,
            "Hospital appointment"
        )

        # Doctor calendar
        create_calendar_event(
            slot.doctor,
            f"Appointment with {request.user.username}",
            start_dt,
            end_dt,
            "Hospital appointment"
        )

    return redirect('patient_slots')

@login_required
def doctor_bookings(request):
    if request.user.role != 'doctor':
        return redirect('dashboard')

    bookings = Booking.objects.filter(slot__doctor=request.user)

    return render(
        request,
        'bookings/doctor_bookings.html',
        {'bookings': bookings}
    )
