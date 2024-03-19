from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import YourItemModel
from .utils import user_based_collaborative_filtering
from .form import ReviewForm
from .models import Staff, Items, Testimonial, Booking, Contact, OrderItem, Customer, Order, ShippingAddress, ReviewRating
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.http import JsonResponse
import json
import datetime

# Create your views here.
def your_view(request):
    # Your existing logic to fetch items from the database
    items = YourItemModel.objects.all()
    # Assuming you have a variable for currency symbol
    currency_symbol = "Rs"  # Or retrieve it from your settings or database
    return render(request, 'index.html', {'items': items, 'currency_symbol': currency_symbol})


def index(request):
    if 'q' in request.GET:
        q = request.GET['q']
        items = Items.objects.filter(name__icontains= q)
    else:
        items = Items.objects.all()
    context = {"items": items,
                "teams": Staff.objects.all(),
                "as": Testimonial.objects.all()
                }
    return render(request, "index.html", context)


def about(request):
    return render(request, template_name="about.html")


def booking(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        datetime = request.POST.get("datetime")
        no_of_people = request.POST.get("no_of_people")
        special_request = request.POST.get("special_request")
        Booking.objects.create(name=name, email=email,
                                datetime=datetime,
                                no_of_people=no_of_people,
                                special_request=special_request
                                )
        return redirect("booking")
    return render(request, template_name="booking.html")


@login_required(login_url='login')
@staff_member_required
def staff_page(request):
    context = {"booking_infos": Booking.objects.all(),
                "contacts": Contact.objects.all()
                }
    return render(request, "staff-page.html", context)


def recommend_items(request):
    recommendations = user_based_collaborative_filtering(request.user)
    context = {"recommendations": recommendations}
    return render(request, 'recommend_items.html', context)


def menu(request):
    context = {
        "review_items": ReviewRating.objects.all(),
        "items": Items.objects.all(),
    }
    return render(request, "menu.html", context)


def service(request):
    return render(request, template_name="service.html")


def team(request):
    context = {
    "teams": Staff.objects.all(),
    }
    return render(request, "team.html", context)


def testimonial(request):
    if request.method == "POST":
        name = request.POST.get("name")
        message = request.POST.get("message")
        Testimonial.objects.create(name=name,
                                    message=message
                                    )
        return redirect("testimonial")
    context = {"title": "testimonial", "as": Testimonial.objects.all()}
    return render(request, "testimonial.html", context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        Contact.objects.create(name=name,
                                email=email,
                                subject=subject,
                                message=message
                                )
        return redirect("contact")
    context = {"title": "contact"}
    return render(request, "contact.html", context)


def delete(request, id):

    try:
        booking = Booking.objects.get(id=id)
    except Booking.DoesNotExist:
        return redirect('staff_page')
    context = {
        "title": "delete", "booking": booking,
    }
    if request.method == "POST":
        Booking.objects.filter(id=id).delete()
        return redirect('staff_page')
    return render(request, "delete.html", context)


def delete_contact(request, id):

    try:
        contact = Contact.objects.get(id=id)
    except Contact.DoesNotExist:
        return redirect('staff_page')
    context = {
        "title": "delete", "contact": contact,
    }
    if request.method == "POST":
        Contact.objects.filter(id=id).delete()
        return redirect('staff_page')
    return render(request, "delete-contact.html", context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        try:
            c = json.loads(request.COOKIES['cart'])
        except:
            c = {}
        order = {"get_cart_items": 0, "get_cart_total": 0}
        cart_items = 0
        items = []
        for product_id in c:
            cart_items += c[product_id]['quantity']
            product = Items.objects.get(id=product_id)
            total = product.price * c[product_id]['quantity']
            order["get_cart_total"] += total
            order["get_cart_items"] += c[product_id]['quantity']

            item = {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "imageURL": product.image.url,
                },
                "quantity": c[product_id]["quantity"],
                "get_total": total
            }
            items.append(item)
    context = {"items": items, "order": order, "cart_items":cart_items}
    return render(request, 'cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        try:
            c = json.loads(request.COOKIES['cart'])
        except:
            c = {}
        order = {"get_cart_items": 0, "get_cart_total": 0}
        cart_items = 0
        items = []
        for product_id in c:
            cart_items += c[product_id]['quantity']
            product = Items.objects.get(id=product_id)
            total = product.price * c[product_id]['quantity']
            order["get_cart_total"] += total
            order["get_cart_items"] += c[product_id]['quantity']

            item = {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "image": {"url": product.image.url}
                },
                "quantity": c[product_id]["quantity"],
                "get_total": total
            }
            items.append(item)
    context = {"items": items, "order": order, "cart_items":cart_items}
    return render(request, 'checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productID']
    action = data['action']

    customer = request.user.customer
    product = Items.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(product=product, order=order)
    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1
    order_item.save()
    if order_item.quantity <= 0:
        order_item.delete()
    response = {
        "message": "Updated Successfully"
    }
    return JsonResponse(response)


def process_order(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        name = data['form']['name']
        email = data['form']['email']
        try:
            c = json.loads(request.COOKIES['cart'])
        except:
            c = {}
        o = {"get_cart_items": 0, "get_cart_total": 0}
        cart_items = 0
        items = []
        for product_id in c:
            cart_items += c[product_id]['quantity']
            product = Items.objects.get(id=product_id)
            total = product.price * c[product_id]['quantity']
            print("order = ", o)
            o["get_cart_total"] += total
            o["get_cart_items"] += c[product_id]['quantity']

            item = {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "imageURL": product.image.url,
                },
                "quantity": c[product_id]["quantity"],
                "get_total": total
            }
            items.append(item)
            customer, created = Customer.objects.get_or_create(email=email)
            customer.name = name
            customer.save()
            order = Order.objects.create(customer=customer, complete=False)
            for item in items:
                product = Items.objects.get(id=item['product']['id'])
                order_item = OrderItem.objects.create(product=product, order=order, quantity=item['quantity'])

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )

    return JsonResponse({
        "message": "Payment Complete"
    })


def send_email(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        from_email = request.POST['from_email']
        recipient_email = request.POST['recipient_email']
        send_mail(subject, message, from_email, [recipient_email])
        return redirect("send_email")

    context = {"title": "Email"}
    return render(request, "send-email.html", context)

def submit_review(request, item_id):
    url = request.META.get("HTTP_REFERER")

    if request.method == "POST":
        try:
            review = ReviewRating.objects.get(user__id=request.user.id, item__id=item_id)
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you for updating your review!')
            else:
                messages.error(request, 'Failed to update the review. Please check your input.')
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.item_id = item_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you for your review!')
            else:
                messages.error(request, 'Failed to submit the review. Please check your input.')

    return redirect(url)

