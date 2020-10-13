from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name;

class Category(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name;

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    category = models.ManyToManyField(Category, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='product/')
    on_sell = models.BooleanField(default=False, null=True)
    date = models.DateTimeField(default=timezone.now)
    on_stock = models.BooleanField(default=True, null=True)
    delivery = models.BooleanField(default=False, null=True)


    def __str__(self):
        return self.name;

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 250 or img.width > 250:
            output_size = (250, 250)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(default=0, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.product)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.product)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    order_placed = models.BooleanField(default = False, null=True, blank=True)
    order_packed = models.BooleanField(default = False, null=True, blank=True)
    order_shipping = models.BooleanField(default = False, null=True, blank=True)
    order_shipped = models.BooleanField(default = False, null=True, blank=True)

    def __str__(self):
        return 'Order ID : ' +  str(self.id)

    @property
    def get_cart_total(self):
        items = self.orderitem_set.all()
        total = sum([item.get_total for item in items])
        return total

    @property
    def get_cart_total_item(self):
        items = self.orderitem_set.all()
        total = sum([item.quentity for item in items])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    quentity = models.IntegerField(default=0, null=True, blank=True)
    date =  models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'OrderItem | Order ID: ' + str(self.order.id)

    @property
    def get_total(self):
        total = self.product.price * self.quentity
        return total


class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zip = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.address
