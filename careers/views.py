from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JobPosting
from .forms import JobPostingForm

def careers_list(request):
    jobs = JobPosting.objects.filter(is_active=True)
    return render(request, 'careers/list.html', {'jobs': jobs})

def job_detail(request, pk):
    job = get_object_or_404(JobPosting, pk=pk, is_active=True)
    return render(request, 'careers/detail.html', {'job': job})

@login_required
def add_job(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('careers:list')
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job posting added!')
            return redirect('dashboard:admin_careers')
    else:
        form = JobPostingForm()
    return render(request, 'careers/form.html', {'form': form, 'title': 'Add Job Posting'})

@login_required
def delete_job(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('careers:list')
    job = get_object_or_404(JobPosting, pk=pk)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job posting deleted.')
        return redirect('dashboard:admin_careers')
    return render(request, 'careers/confirm_delete.html', {'job': job})
