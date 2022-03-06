from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Order, Customer


@receiver(pre_save, sender=Order)
def update_order(sender, instance, *args, **kwargs):
    if instance.complete:
        instance.order_placed = False
        instance.order_packed = False
        instance.order_shipping = False
        instance.order_shipped = False
        instance.custom = False
        instance.complete = False
        orderitems = instance.orderitem_set.all()
        for item in orderitems:
            item.delete()

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, *args, **kwargs):
    if created:
        Customer.objects.create(user=instance, email=instance.email, name=instance.first_name+" "+instance.last_name+" "+instance.username)
