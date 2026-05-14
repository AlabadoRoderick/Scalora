from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Blog
from .forms import BlogForm

def blog_list(request):
    blogs = Blog.objects.filter(is_published=True)
    return render(request, 'blogs/list.html', {'blogs': blogs})

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_published=True)
    related = Blog.objects.filter(is_published=True).exclude(pk=blog.pk)[:3]
    return render(request, 'blogs/detail.html', {'blog': blog, 'related': related})

@login_required
def add_blog(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('blogs:list')
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog post published!')
            return redirect('dashboard:admin_blogs')
    else:
        form = BlogForm()
    return render(request, 'blogs/form.html', {'form': form, 'title': 'Add Blog Post'})

@login_required
def edit_blog(request, slug):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('blogs:list')
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated!')
            return redirect('dashboard:admin_blogs')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blogs/form.html', {'form': form, 'title': 'Edit Blog Post', 'blog': blog})

@login_required
def delete_blog(request, slug):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('blogs:list')
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog post deleted.')
        return redirect('dashboard:admin_blogs')
    return render(request, 'blogs/confirm_delete.html', {'blog': blog})
