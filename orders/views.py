import stripe
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from shop_cart.models import Cart
from .models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('shop_cart:cart')

    if request.method == 'POST':
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        if payment_method not in ["CARD", "COD"]:
            return redirect('shop_cart:cart')


        total = sum(item.product.price * item.quantity for item in cart_items)

        order = Order.objects.create(
            user=request.user,
            address=address,
            payment_method=payment_method,
            total_price=total,
            is_paid=False
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        if payment_method == "CARD":
            line_items = []

            for item in cart_items:
                line_items.append({
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': item.product.name,
                        },
                        'unit_amount': int(item.product.price * 100),
                    },
                    'quantity': item.quantity,
                })

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri(
                    reverse('orders:success', args=[order.id])
                ),
                cancel_url=request.build_absolute_uri(
                    reverse('orders:cancel')
                ),
            )

            return redirect(session.url)
        elif payment_method == "COD":
            return redirect('orders:success', order.id)

    return render(request, 'checkout.html', {'cart_items': cart_items})


@login_required
def success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.payment_method == "CARD":
        order.is_paid = True
        order.save()

    Cart.objects.filter(user=request.user).delete()
    return render(request, 'success.html', {'order': order})


@login_required
def cancel(request):
    return redirect('shop_cart:cart')
