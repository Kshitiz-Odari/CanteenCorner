from django.contrib import admin
from .models import Staff, Items, Testimonial, Booking, Contact, Customer, Order, OrderItem, ShippingAddress, ReviewRating
# Register your models here.
admin.site.register(Staff)
admin.site.register(Items)
admin.site.register(Testimonial)
admin.site.register(Booking)
admin.site.register(Contact)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(ReviewRating)