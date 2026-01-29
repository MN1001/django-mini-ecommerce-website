from django.urls import path
from . import views

app_name = 'shop_cart'

urlpatterns = [
    path('cart/',views.cartview,name="cart"),
    path('addcart/<int:id>/',views.addtocart,name="addcart"),
    path('cartdel/<int:id>/',views.cartdel,name="cartdel"),
]