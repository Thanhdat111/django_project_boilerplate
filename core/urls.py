from django.urls import path
from .views import (
    check_out,
    add_to_cart,
    ProductDetailView,
    HomeView,
    remove_from_cart
)

app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout', check_out, name='check_out'),
    # pass url
    path('product/<slug>', ProductDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>',add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart')
]
