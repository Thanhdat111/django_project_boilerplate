from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.


class HomeView(ListView):
    model = Item
    template_name = "home-page.html"


# def items_list(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "home-page.html", context)

class ProductDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'


def check_out(request):
    return render(request, 'checkout-page.html')


@login_required()
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    # get or create object when add to cart
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            # order items already in the cart
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item was updated.")
        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)

    else:
        # add order_date
        ordered_dated = timezone.now()
        order = Order.objects.create(
            user=request.user,
            order_date=ordered_dated)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
    return redirect("core:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            # order items already in the cart
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart")
        else:
            # add a mesage saying the user dosenot item
            messages.info(request, "This item doesnt in your cart")
            return redirect("core:product", slug=slug)
    else:
        # add a message saying the user doesnt have on order
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)
