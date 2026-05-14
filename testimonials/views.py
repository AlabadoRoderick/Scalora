from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Testimonial
from .forms import TestimonialForm

def testimonials_list(request):
    testimonials = Testimonial.objects.filter(is_active=True)
    return render(request, 'testimonials/list.html', {'testimonials': testimonials})

@login_required
def add_testimonial(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('testimonials:list')
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial added!')
            return redirect('dashboard:admin_testimonials')
    else:
        form = TestimonialForm()
    return render(request, 'testimonials/form.html', {'form': form, 'title': 'Add Testimonial'})

@login_required
def edit_testimonial(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('testimonials:list')
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial updated!')
            return redirect('dashboard:admin_testimonials')
    else:
        form = TestimonialForm(instance=testimonial)
    return render(request, 'testimonials/form.html', {'form': form, 'title': 'Edit Testimonial', 'testimonial': testimonial})

@login_required
def delete_testimonial(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('testimonials:list')
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        testimonial.delete()
        messages.success(request, 'Testimonial deleted.')
        return redirect('dashboard:admin_testimonials')
    return render(request, 'testimonials/confirm_delete.html', {'testimonial': testimonial})