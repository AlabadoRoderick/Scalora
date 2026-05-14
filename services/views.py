from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Service, AdminSchedule
from .forms import ServiceForm, AdminScheduleForm


def services_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'services/services_list.html', {'services': services})


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk, is_active=True)
    return render(request, 'services/service_detail.html', {'service': service})


@login_required
def add_service(request):
    if not (request.user.is_staff or hasattr(request.user, 'profile') and request.user.profile.is_admin()):
        messages.error(request, 'Access denied.')
        return redirect('services:list')
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added successfully!')
            return redirect('dashboard:admin_services')
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form, 'title': 'Add Service'})


@login_required
def edit_service(request, pk):
    if not (request.user.is_staff or hasattr(request.user, 'profile') and request.user.profile.is_admin()):
        messages.error(request, 'Access denied.')
        return redirect('services:list')
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully!')
            return redirect('dashboard:admin_services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form, 'title': 'Edit Service', 'service': service})


@login_required
def delete_service(request, pk):
    if not (request.user.is_staff or hasattr(request.user, 'profile') and request.user.profile.is_admin()):
        messages.error(request, 'Access denied.')
        return redirect('services:list')
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted.')
        return redirect('dashboard:admin_services')
    return render(request, 'services/service_confirm_delete.html', {'service': service})


@login_required
def toggle_schedule(request, pk):
    if not (request.user.is_staff or hasattr(request.user, 'profile') and request.user.profile.is_admin()):
        return JsonResponse({'error': 'Access denied'}, status=403)
    slot = get_object_or_404(AdminSchedule, pk=pk)
    if request.method == 'POST':
        slot.is_available = not slot.is_available
        slot.save()
        return JsonResponse({'is_available': slot.is_available, 'pk': slot.pk})
    return JsonResponse({'error': 'POST required'}, status=405)


@login_required
def delete_schedule(request, pk):
    if not (request.user.is_staff or hasattr(request.user, 'profile') and request.user.profile.is_admin()):
        messages.error(request, 'Access denied.')
        return redirect('dashboard:admin_services')
    slot = get_object_or_404(AdminSchedule, pk=pk)
    if request.method == 'POST':
        slot.delete()
        messages.success(request, 'Schedule slot removed.')
    return redirect('dashboard:admin_services')


def get_available_dates(request):
    """API: returns all dates that have at least one open slot, for a given year-month."""
    from bookings.models import Appointment
    from datetime import date
    year  = request.GET.get('year')
    month = request.GET.get('month')
    if not year or not month:
        return JsonResponse({'dates': []})
    try:
        year, month = int(year), int(month)
    except ValueError:
        return JsonResponse({'dates': []})

    schedules = AdminSchedule.objects.filter(
        date__year=year, date__month=month, is_available=True
    )
    booked = Appointment.objects.filter(
        date__year=year, date__month=month, status__in=['pending', 'confirmed']
    ).values('date').annotate(cnt=__import__('django.db.models', fromlist=['Count']).Count('id'))
    booked_counts = {b['date'].isoformat(): b['cnt'] for b in booked}

    available = set()
    from datetime import datetime, timedelta
    for s in schedules:
        current = datetime.combine(s.date, s.start_time)
        end     = datetime.combine(s.date, s.end_time)
        while current + timedelta(minutes=30) <= end:
            slot_time = current.time()
            # check if this slot is already booked
            key = s.date.isoformat()
            already = Appointment.objects.filter(
                date=s.date, time_slot=slot_time, status__in=['pending', 'confirmed']
            ).exists()
            if not already:
                available.add(s.date.isoformat())
                break
            current += timedelta(minutes=30)

    return JsonResponse({'dates': sorted(available)})


def get_available_slots(request):
    """API endpoint for calendar - returns available slots as JSON"""
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'slots': []})
    from bookings.models import Appointment
    from datetime import date
    try:
        selected_date = date.fromisoformat(date_str)
    except ValueError:
        return JsonResponse({'slots': []})
    schedules = AdminSchedule.objects.filter(date=selected_date, is_available=True)
    booked_slots = Appointment.objects.filter(
        date=selected_date, status__in=['pending', 'confirmed']
    ).values_list('time_slot', flat=True)
    slots = []
    for s in schedules:
        from datetime import datetime, timedelta
        current = datetime.combine(selected_date, s.start_time)
        end = datetime.combine(selected_date, s.end_time)
        while current + timedelta(minutes=30) <= end:
            slot_time = current.time()
            if slot_time not in booked_slots:
                slots.append(slot_time.strftime('%H:%M'))
            current += timedelta(minutes=30)
    return JsonResponse({'slots': slots})


@login_required
def toggle_schedule(request, pk):
    """Admin only - toggle a schedule slot available/blocked"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:admin_services')
    slot = get_object_or_404(AdminSchedule, pk=pk)
    if request.method == 'POST':
        slot.is_available = not slot.is_available
        slot.save()
        status = 'Available' if slot.is_available else 'Blocked'
        messages.success(request, f'Slot on {slot.date} at {slot.start_time.strftime("%I:%M %p")} marked as {status}.')
    return redirect('dashboard:admin_services')


@login_required
def delete_schedule(request, pk):
    """Admin only - delete a schedule slot"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:admin_services')
    slot = get_object_or_404(AdminSchedule, pk=pk)
    if request.method == 'POST':
        slot.delete()
        messages.success(request, 'Schedule slot removed.')
    return redirect('dashboard:admin_services')


@login_required
def toggle_schedule(request, pk):
    """Toggle a schedule slot's availability status."""
    if not (request.user.is_staff or hasattr(request.user, 'profile') and request.user.profile.is_admin()):
        return JsonResponse({'error': 'Access denied'}, status=403)
    slot = get_object_or_404(AdminSchedule, pk=pk)
    if request.method == 'POST':
        slot.is_available = not slot.is_available
        slot.save()
    from django.shortcuts import redirect
    return redirect('dashboard:admin_services')


@login_required
def delete_schedule(request, pk):
    """Delete a schedule slot."""
    if not (request.user.is_staff or hasattr(request.user, 'profile') and request.user.profile.is_admin()):
        return JsonResponse({'error': 'Access denied'}, status=403)
    slot = get_object_or_404(AdminSchedule, pk=pk)
    if request.method == 'POST':
        slot.delete()
    from django.shortcuts import redirect
    return redirect('dashboard:admin_services')