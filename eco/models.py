from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.template.defaultfilters import slugify
from django.template.defaultfilters import truncatechars
# from django.db.models.signals import post_save
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from multiselectfield import MultiSelectField
from mptt.models import MPTTModel, TreeForeignKey


MEDIA_CHOICES = [

    ('MAN', (
            ('shoe', 'Shoe'),
            ('shirt', 'Shirt'),
            ('watch', 'Watch'),
        )
    ),
    ('LADIES', (
            ('cream', 'Cream'),
            ('glass', 'Glass'),
            ('ring', 'Ring'),
        )

    ),
    ('ELECTORNIC', (
            ('phone', 'Phone'),
            ('lapton', 'Laptop'),
            ('speaker', 'Speaker'),
            ('cleaner', 'Cleaner'),
            ('dvd', 'DVD'),
        )
    ),

            ]
  
LABEL_CHOICES = (
    ('N', 'NEW'),
    ('G', 'GIFT'),
    ('O', 'OFFER')
)
LABEL_CHOICES = (
    ('N', 'NEW'),
    ('G', 'GIFT'),
    ('O', 'OFFER')
)
LABEL_CHOICES = (
    ('N', 'NEW'),
    ('G', 'GIFT'),
    ('O', 'VIP')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)


    def __str__(self):
        return str(self.user)

# class Category(models.Model):
#     name = models.CharField(max_length=50, blank=True)

#     def __str__(self):
#         return self.name


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = TreeForeignKey('Category', related_name='categories', on_delete=models.CASCADE,null=True,blank=True)
    label1 = models.CharField(choices=LABEL_CHOICES, max_length=1, blank=True)
    label2 = models.CharField(choices=LABEL_CHOICES, max_length=1, blank=True)
    label3 = models.CharField(choices=LABEL_CHOICES, max_length=1, blank=True)
    image = models.ImageField(upload_to='productpic')
    description = models.TextField
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("eco:EcoDetail", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("eco:add-to-cart", kwargs={
            'slug': self.slug
        })

  
    def get_remove_from_cart_url(self):
        return reverse("eco:remove-from-cart", kwargs={
            'slug': self.slug
        })
    def get_remove_from_singel_cart_url(self):
        return reverse("eco:remove_single_item_from_cart", kwargs={
            'slug': self.slug
        })
    def get_add_to_wish_url(self):
        return reverse("eco:add-to-wish", kwargs={
            'slug': self.slug
        })
        
    def get_remove_to_wish_url(self):
        return reverse("eco:remove-to-wish", kwargs={
            'slug': self.slug
        })
        

    
    # @property 
    # def imageURL(self):
    #     try:
    #         url = self.image.url
    #     except:
    #         url = ''
    #     return url

class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', db_index=True)
    slug = models.SlugField(null=False, unique=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("eco:CategoryDetail", kwargs={
            'slug': self.slug
        })

    class MPTTMeta:
        order_insertion_by = ['name']

    


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return str(self.item)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    wishlist = models.ManyToManyField(Wishlist, blank=True)
 

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    def get_final_price_list(self):
        if self.item.discount_price:
            return self.get_amount_saved()
        return self.get_total_item_price()


   
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)



    def __str__(self):
        return str(self.user)


    # def get_total(self):
    #     total = 0
    #     for order_item in self.items.all():
    #         total += order_item.get_amount_saved()
    #     return total


       

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price_list()
        return total

    def get_total_full(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price_list()
        if self.coupon:
            total -= self.coupon.amount
        return total




class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stripe_charge_id


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

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
