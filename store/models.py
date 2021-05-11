from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username;

class Category(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name;

class Product(models.Model):
    '''
    NAME =(
        (value, name)
        database will accept the value while form submission
        if we use name as form value the form will be in valid
    )
    '''
    SIZE = (('s', 's'),
            ('m', 'm'),
            ('l', 'l'),
            ('xl', 'xl'),
            ('xxl', 'xxl'))
    COLOR = (('red', 'red'),
             ('black', 'black'),
             ('blue', 'blue'),
             ('green', 'green'),
             ('white', 'white'),
             ('gray', 'gray'))

    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    old_price = models.FloatField(null=True, blank=True)
    category = models.ManyToManyField(Category)
    image = models.ImageField(null=True, blank=True, upload_to='product/')
    on_sell = models.BooleanField(default=False, null=True)
    date = models.DateTimeField(default=timezone.now)
    on_stock = models.BooleanField(default=True, null=True)
    delivery = models.BooleanField(default=False, null=True)
    color = models.CharField(max_length=200, null=True, blank=True, choices=COLOR)
    size = models.CharField(max_length=200, null=True, blank=True, choices=SIZE)

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

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
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    order_placed = models.BooleanField(default = False)
    order_packed = models.BooleanField(default = False)
    order_shipping = models.BooleanField(default = False)
    order_shipped = models.BooleanField(default = False)
    custom = models.BooleanField(default=False)

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
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zip = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.address

class Custom(models.Model):
    DESIGN_SIZE = (
        ('large', 'large'),
        ('medium', 'medium'),
        ('small', 'small'),
    )
    TSHIRT_SIZE = (
        ('s', 's'),
        ('m', 'm'),
        ('l', 'l'),
        ('xl', 'xl'),
        ('xxl', 'xxl')
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="custom_order", blank=True, null=True)
    design = models.ImageField(null=True, blank=False, upload_to="custom/")
    color = models.CharField(max_length=100, null=True, blank=False)
    tshirt_size = models.CharField(max_length=100, null=True, blank=False, choices=TSHIRT_SIZE)
    design_size = models.CharField(max_length=100, null=True, blank=False, choices=DESIGN_SIZE)
    quentity = models.CharField(default="1", max_length=200, null=True, blank=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.customer.user.username

    def save(self, *args, **kwargs):
        super(Custom, self).save(*args, **kwargs)

        img = Image.open(self.design.path)

        if img.height > 1000 or img.width > 1000:
            output_size = (1000, 1000)
            img.thumbnail(output_size)
            img.save(self.design.path)
