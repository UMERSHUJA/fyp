from datetime import datetime
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField


CATEGORY_CHOICES =(
        ('Mobile', 'Mobile'),
        ('Computer', 'Computer'),
        ('Television', 'Television'),
        ('Audio', 'Audio'),
        ('LargeAppliances', 'Large Appliances'),
        ('Camera', 'Camera')
    )


LABEL_CHOICES =(
        ('p', 'primary'),
        ('S', 'secondary'),
        ('D', 'danger')
        
    )


ADDRESS_CHOICES =(
        ('B', 'Billing'),
        ('S', 'Shipping'),
        
    )


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(default=0)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=15)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1,blank=True, null=True)
    is_published = models.BooleanField(default=True)
    stock = models.IntegerField(default=100)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    image_1 = models.ImageField(upload_to='photos/%Y/%m/%d')    
    image_2 = models.ImageField(upload_to='photos/%Y/%m/%d')

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("core:product", kwargs={      # core is the namespace, and product is the name of the url.
            'slug': self.slug
            })


    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={      # core is the namespace, and add-to-cart is the name of the url.
            'slug': self.slug
            })



    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={      # core is the namespace, and remove-from-cart is the name of the url.
            'slug': self.slug
            })


    def get_price(self):
        return self.price - self.discount_price




class OrderItem(models.Model): 
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    
    def get_total_item_price(self):
        return self.quantity * self.item.price


    def get_total_discount_item_price(self):
        return self.quantity * (self.item.price - self.item.discount_price)



    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()


    def get_final_price(self):
        if self.item.discount_price > 0:
            return self.get_total_discount_item_price()
        else:
            return self.get_total_item_price()



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True) 
    items = models.ManyToManyField(OrderItem)
    item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="OrderItem", blank="True", null="True")
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address= models.ForeignKey('Address', related_name="billing_address", on_delete = models.SET_NULL, blank=True, null=True)
    shipping_address= models.ForeignKey('Address', related_name="shipping_address", on_delete = models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete = models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete = models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    '''
    
    1. Item added to the cart
    2. Addnig a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delievred
    5. Received
    6. Refunds

    '''

    def __str__(self):
        return self.user.username


    def get_item_info(self):
        quantity = self.items.quantity
        return quantity


    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Comment(models.Model):
    order = models.CharField(max_length=30)
    message = models.CharField(max_length=200, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.order


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                            on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False, default='Pakistan')
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
    requested_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
       return f"{self.pk}"



def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)





