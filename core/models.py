from django.db import models
from django.utils import timezone
# Create your models here.
from django.db import models
from django.conf import settings
from django.shortcuts import reverse

CATEGORY_CHOICE = (
    ('S', 'Shirt'),
    ('SW', 'Sport Wear'),
    ('OW', 'Out Wear')
)
LABEL_CHOICE = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


class Item(models.Model):
    title = models.CharField(max_length=180)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICE, default='S', max_length=2)
    label = models.CharField(choices=LABEL_CHOICE, default='P', max_length=2)
    slug = models.SlugField(default='product')
    description = models.TextField()

    def get_absolute_url(self):
        # same name with name url
        # path('product/<slug>', product_detail, name='product')
        return reverse("core:product", kwargs={
            # pass slug to url
            'slug': self.slug
        })

    # get url add to cart
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            # pass slug to url
            'slug': self.slug
        })

    # get url remove from cart
    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            # pass slug to url
            'slug': self.slug
        })

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateField(default=timezone.now())
    order_date = models.DateField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username






