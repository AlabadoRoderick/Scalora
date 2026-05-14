from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Appointment
from .forms import AppointmentForm


def send_booking_emails(appointment):
    """Send email notifications to both client and admin."""
    context = {
        'appointment': appointment,
        'client_name': appointment.client.get_full_name() or appointment.client.username,
        'service_name': appointment.service.name,
        'date': appointment.date,
        'time': appointment.time_slot.strftime('%I:%M %p'),
    }

    # Email to client
    client_subject = f'Booking Confirmed – {appointment.service.name} on {appointment.date}'
    client_message = f"""
Dear {context['client_name']},

Your appointment has been successfully booked!

BOOKING DETAILS:
─────────────────────────────
Service: {context['service_name']}
Date: {appointment.date.strftime('%B %d, %Y')}
Time: {context['time']}
Status: {appointment.get_status_display()}
─────────────────────────────

If you need to make changes, please log in to your Scalora dashboard.

Thank you for choosing Scalora!

Best regards,
The Scalora Team
"""

    # Email to admin
    admin_subject = f'New Booking: {appointment.service.name} – {context['client_name']}'
    admin_message = f"""
New appointment booking received!

CLIENT: {context['client_name']} ({appointment.client.email})
SERVICE: {context['service_name']}
DATE: {appointment.date.strftime('%B %d, %Y')}
TIME: {context['time']}
NOTES: {appointment.notes or 'None'}

Booking ID: #{appointment.pk}

Log in to the admin dashboard to manage this booking.
"""

    try:
        send_mail(
            client_subject, client_message,
            settings.DEFAULT_FROM_EMAIL,
            [appointment.client.email],
            fail_silently=True
        )
        send_mail(
            admin_subject, admin_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=True
        )
    except Exception:
        pass  # Email failures shouldn't break booking flow


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.save()
            send_booking_emails(appointment)
            messages.success(request, f'Your appointment for {appointment.service.name} on {appointment.date} at {appointment.time_slot.strftime("%I:%M %p")} has been booked! A confirmation email has been sent.')
            return redirect('dashboard:client_bookings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AppointmentForm()
    return render(request, 'bookings/book_appointment.html', {'form': form})


@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, client=request.user)
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Your appointment has been cancelled.')
        return redirect('dashboard:client_bookings')
    return render(request, 'bookings/cancel_confirm.html', {'appointment': appointment})


@login_required
def appointment_detail(request, pk):
    if request.user.is_staff:
        appointment = get_object_or_404(Appointment, pk=pk)
    else:
        appointment = get_object_or_404(Appointment, pk=pk, client=request.user)
    return render(request, 'bookings/appointment_detail.html', {'appointment': appointment})


@login_required
def update_appointment_status(request, pk):
    """Admin only - update booking status, optionally attach a Meet link"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        meet_link = request.POST.get('meet_link', '').strip()
        if status in ['pending', 'confirmed', 'cancelled', 'completed']:
            prev_status = appointment.status
            appointment.status = status
            if meet_link:
                appointment.meet_link = meet_link
            appointment.save()

            # Send confirmation email with Meet link when confirming
            if status == 'confirmed' and meet_link:
                client_name = appointment.client.get_full_name() or appointment.client.username
                try:
                    send_mail(
                        f'Appointment Confirmed – {appointment.service.name} on {appointment.date}',
                        f"""Dear {client_name},

Your appointment has been confirmed!

BOOKING DETAILS:
─────────────────────────────
Service : {appointment.service.name}
Date    : {appointment.date.strftime('%B %d, %Y')}
Time    : {appointment.time_slot.strftime('%I:%M %p')}
Status  : Confirmed
─────────────────────────────

🎥 JOIN YOUR MEETING:
{meet_link}

Please click the link above at your scheduled time. Make sure your camera and microphone are ready.

If you need to reschedule, please log in to your Scalora dashboard.

Best regards,
The Scalora Team
""",
                        settings.DEFAULT_FROM_EMAIL,
                        [appointment.client.email],
                        fail_silently=True,
                    )
                except Exception:
                    pass

            messages.success(request, f'Booking #{appointment.pk} updated to {appointment.get_status_display()}'
                             + (' and Meet link sent to client.' if status == 'confirmed' and meet_link else '.'))
    return redirect('dashboard:admin_bookings')