from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
# # Create your models here.

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')

)

class YourItemModel(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='img/')
    # Add any other fields as needed


class Staff(models.Model):
    name = models.CharField(max_length=20)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=50, null=True)
    designation = models.CharField(max_length=20, null=True)
    facebook = models.CharField(max_length=200, null=True)
    linkedin = models.CharField(max_length=200, null=True)
    instagram = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Items(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    digital = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"


class ReviewRating(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0.5), MaxValueValidator(5.0)])

    def __str__(self):
        return f"Rating for {self.item.name} by {self.user.username}: {self.rating}"

    def clean(self):
        if not (0.5 <= self.rating <= 5.0):
            raise ValidationError('Rating must be between 0.5 and 5.0.')

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=12)
    orders = models.ManyToManyField(Items, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if not i.product.digital:
                shipping = True
                break
        return shipping


class OrderItem(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Items, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.quantity * self.product.price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=100, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Testimonial(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=True)
    message = models.TextField(max_length=100, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Booking(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=50, null=True)
    datetime = models.DateTimeField(auto_now_add=True,null=True)
    no_of_people = models.IntegerField(null=True)
    special_request = models.TextField(max_length=200, null=True)
    pre_order = models.ManyToManyField(Items, blank=True)
    date_booked = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Contact(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=300)
    date_messaged = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"


