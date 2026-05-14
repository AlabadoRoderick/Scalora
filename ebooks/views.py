from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Ebook, EbookOrder
from .forms import EbookForm, OrderForm

def ebook_store(request):
    ebooks = Ebook.objects.filter(is_active=True)
    return render(request, 'ebooks/store.html', {'ebooks': ebooks})

def ebook_detail(request, pk):
    ebook = get_object_or_404(Ebook, pk=pk, is_active=True)
    return render(request, 'ebooks/detail.html', {'ebook': ebook})

@login_required
def order_ebook(request, pk):
    ebook = get_object_or_404(Ebook, pk=pk, is_active=True)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user
            order.ebook = ebook
            order.total_price = ebook.price * order.quantity
            order.save()
            # Notify admin
            try:
                send_mail(
                    f'New eBook Order: {ebook.title}',
                    f'New order from {request.user.get_full_name() or request.user.username}\n'
                    f'eBook: {ebook.title}\nQty: {order.quantity}\nTotal: ${order.total_price}\n'
                    f'Notes: {order.notes or "None"}\n\nOrder ID: #{order.pk}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
                send_mail(
                    f'Your Scalora eBook Order – {ebook.title}',
                    f'Thank you for your order!\n\nYou ordered: {ebook.title}\n'
                    f'Quantity: {order.quantity}\nTotal: ${order.total_price}\n\n'
                    f'Our team will contact you shortly with payment instructions.\n\nOrder ID: #{order.pk}',
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, f'Your order for "{ebook.title}" has been placed! We will contact you with payment details.')
            return redirect('dashboard:client_orders')
    else:
        form = OrderForm()
    return render(request, 'ebooks/order.html', {'form': form, 'ebook': ebook})

@login_required
def add_ebook(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('ebooks:store')
    if request.method == 'POST':
        form = EbookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'eBook added to store!')
            return redirect('dashboard:admin_ebooks')
    else:
        form = EbookForm()
    return render(request, 'ebooks/form.html', {'form': form, 'title': 'Add eBook'})

@login_required
def edit_ebook(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('ebooks:store')
    ebook = get_object_or_404(Ebook, pk=pk)
    if request.method == 'POST':
        form = EbookForm(request.POST, request.FILES, instance=ebook)
        if form.is_valid():
            form.save()
            messages.success(request, 'eBook updated!')
            return redirect('dashboard:admin_ebooks')
    else:
        form = EbookForm(instance=ebook)
    return render(request, 'ebooks/form.html', {'form': form, 'title': 'Edit eBook', 'ebook': ebook})

@login_required
def update_order_status(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    order = get_object_or_404(EbookOrder, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        transaction_id = request.POST.get('transaction_id', '')
        if status in ['pending', 'confirmed', 'delivered', 'cancelled']:
            order.status = status
            if transaction_id:
                order.transaction_id = transaction_id
            order.save()
            messages.success(request, 'Order updated.')
    return redirect('dashboard:admin_ebooks')

@login_required
def generate_receipt(request, pk):
    if request.user.is_staff:
        order = get_object_or_404(EbookOrder, pk=pk)
    else:
        order = get_object_or_404(EbookOrder, pk=pk, client=request.user)
    return render(request, 'ebooks/receipt.html', {'order': order})
