from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from store.models import Product
from .models import Cart

# Create your views here.

@login_required
def addtocart(request,id):
    p = Product.objects.get(id=id)
    cart_item,created = Cart.objects.get_or_create(product=p,user=request.user)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('shop_cart:cart')

@login_required
def cartview(request):
    p = Cart.objects.filter(user=request.user)
    return render(request,'cart.html',{'data':p})

@login_required
def cartdel(request,id):
    cart_item = Cart.objects.get(id=id,user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('shop_cart:cart')