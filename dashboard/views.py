from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bookings.models import Appointment
from services.models import Service
from testimonials.models import Testimonial
from blogs.models import Blog
from careers.models import JobPosting
from ebooks.models import Ebook, EbookOrder
from accounts.models import UserProfile


def is_admin_user(user):
    return user.is_staff or (hasattr(user, 'profile') and user.profile.role == 'admin')


@login_required
def dashboard_index(request):
    if is_admin_user(request.user):
        return redirect('dashboard:admin_home')
    return redirect('dashboard:client_home')


@login_required
def admin_home(request):
    if not is_admin_user(request.user):
        messages.error(request, 'Admin access required.')
        return redirect('dashboard:client_home')
    context = {
        'total_bookings': Appointment.objects.count(),
        'pending_bookings': Appointment.objects.filter(status='pending').count(),
        'confirmed_bookings': Appointment.objects.filter(status='confirmed').count(),
        'total_services': Service.objects.count(),
        'total_blogs': Blog.objects.count(),
        'total_jobs': JobPosting.objects.filter(is_active=True).count(),
        'total_ebook_orders': EbookOrder.objects.count(),
        'pending_orders': EbookOrder.objects.filter(status='pending').count(),
        'recent_bookings': Appointment.objects.order_by('-created_at')[:5],
        'recent_orders': EbookOrder.objects.order_by('-ordered_at')[:5],
    }
    return render(request, 'dashboard/admin/home.html', context)


@login_required
def client_home(request):
    context = {
        'my_bookings': Appointment.objects.filter(client=request.user).order_by('-date')[:5],
        'my_orders': EbookOrder.objects.filter(client=request.user).order_by('-ordered_at')[:5],
        'total_bookings': Appointment.objects.filter(client=request.user).count(),
        'total_orders': EbookOrder.objects.filter(client=request.user).count(),
    }
    return render(request, 'dashboard/client/home.html', context)


@login_required
def admin_bookings(request):
    if not is_admin_user(request.user):
        return redirect('dashboard:client_home')
    bookings = Appointment.objects.select_related('client', 'service').order_by('-date', '-time_slot')
    status_filter = request.GET.get('status', '')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    return render(request, 'dashboard/admin/bookings.html', {'bookings': bookings, 'status_filter': status_filter})


@login_required
def client_bookings(request):
    bookings = Appointment.objects.filter(client=request.user).select_related('service').order_by('-date')
    return render(request, 'dashboard/client/bookings.html', {'bookings': bookings})


@login_required
def admin_services(request):
    if not is_admin_user(request.user):
        return redirect('dashboard:client_home')
    services = Service.objects.all()
    from services.models import AdminSchedule
    schedules = AdminSchedule.objects.order_by('date', 'start_time')[:20]
    from services.forms import AdminScheduleForm
    form = AdminScheduleForm()
    if request.method == 'POST':
        form = AdminScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Schedule slot added!')
            return redirect('dashboard:admin_services')
    return render(request, 'dashboard/admin/services.html', {
        'services': services, 'schedules': schedules, 'form': form
    })


@login_required
def admin_testimonials(request):
    if not is_admin_user(request.user):
        return redirect('dashboard:client_home')
    testimonials = Testimonial.objects.all()
    return render(request, 'dashboard/admin/testimonials.html', {'testimonials': testimonials})


@login_required
def admin_blogs(request):
    if not is_admin_user(request.user):
        return redirect('dashboard:client_home')
    blogs = Blog.objects.order_by('-created_at')
    return render(request, 'dashboard/admin/blogs.html', {'blogs': blogs})


@login_required
def admin_careers(request):
    if not is_admin_user(request.user):
        return redirect('dashboard:client_home')
    jobs = JobPosting.objects.all()
    return render(request, 'dashboard/admin/careers.html', {'jobs': jobs})


@login_required
def admin_ebooks(request):
    if not is_admin_user(request.user):
        return redirect('dashboard:client_home')
    ebooks = Ebook.objects.all()
    orders = EbookOrder.objects.select_related('client', 'ebook').order_by('-ordered_at')
    return render(request, 'dashboard/admin/ebooks.html', {'ebooks': ebooks, 'orders': orders})


@login_required
def client_orders(request):
    orders = EbookOrder.objects.filter(client=request.user).select_related('ebook').order_by('-ordered_at')
    return render(request, 'dashboard/client/orders.html', {'orders': orders})
