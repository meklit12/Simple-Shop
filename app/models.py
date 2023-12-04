from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES = [
    ('ML', 'Milk'),
    ('IC', 'Ice-Cream'),
    ('JU', 'juice'),
    ('MS', 'Milkshake'),
    ('CH', 'Checolet'),
    ('CK', 'Cake'),
    ('PS', 'Protien Shake'),
    ('HF', 'Habeshan Food'),
]

STATE_CHOICES = [
    ('Addis-Abeba', 'Addis-Abeba'),
    ('Mekele', 'Mekele'),
    ('Dire-Dawa', 'Dire-Dawa'),
    ('Hawssa', 'Hawssa'),
    ('Bahir-Dar', 'Bahir-Dar'),
    ('Jimma', 'Jimma'),
    ('Hareri', 'Hareri'),
    ('Somali', 'Somali'),
    ('Gambella', 'Gambella'),
]


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.title


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    paypal_order_id = models.CharField(max_length=100, blank=True, null=True)
    paypal_payment_status = models.CharField(
        max_length=100, blank=True, null=True)
    paypal_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)


STATUS_CHOICES = [
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending'),
]


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='Pending')
    # payment = models.ForeignKey(
    #     Payment, on_delete=models.CASCADE, default="")

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
