from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import CustomUserCreationForm
from .models import Cart, CartItem, Category,Product,Order,OrderItem,BillingDetail
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail





# API SECTION START FROM HERE

@csrf_exempt
def category_list(request):
    if request.method == "GET":
        categories = Category.objects.all()
        category_list = [{'id': category.id, 'name': category.name, 'img': category.img.url} for category in categories]
        return JsonResponse(category_list, safe=False)
    
    elif request.method == "POST":
        data = json.loads(request.body)
        category = Category.objects.create(name=data['name'], img=data['img'])
        return JsonResponse({'id': category.id, 'name': category.name, 'img': category.img.url}, status=201)
    

@csrf_exempt
def product_list(request):
    if request.method == "GET":
        products = Product.objects.all()
        product_list = [{
            'id': product.id,
            'category': {
                'id': product.category.id,
                'name': product.category.name  # Include only necessary information about the category
            },
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'image': product.image.url
        } for product in products]
        return JsonResponse(product_list, safe=False)
    
    elif request.method == "POST":
        data = json.loads(request.body)
        category = Category.objects.get(id=data['category_id'])
        product = Product.objects.create(
            category=category,
            name=data['name'],
            description=data['description'],
            price=data['price'],
            image=data['image']
        )
        return JsonResponse({
            'id': product.id,
            'category': {
                'id': product.category.id,
                'name': product.category.name
            },
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'image': product.image.url
        }, status=201)




@csrf_exempt
def user_list(request):
    if request.method == "GET":
        users = User.objects.all()
        user_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        return JsonResponse(user_list, safe=False)
    
    elif request.method == "POST":
        data = json.loads(request.body)
        user = User.objects.create(username=data['username'], email=data['email'])
        return JsonResponse({'id': user.id, 'username': user.username, 'email': user.email}, status=201)


# API SECTION END HERE


def index(request):
    category = Category.objects.all()
    cart_items = []
    total_items_in_cart = 0
    total_price = Decimal('0.00')
    gst = Decimal('0.00')
    total_price_with_gst = Decimal('0.00')

    if request.user.is_authenticated:
        # Retrieve cart items and calculate related values only if the user is authenticated
        cart_items = CartItem.objects.filter(cart__user=request.user)
        print(cart_items)
        total_items_in_cart = cart_items.count()    
        print(total_items_in_cart)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        print(total_price)
        gst = total_price * Decimal('0.18')
        print(gst)
        total_price_with_gst = total_price + gst
        print(total_price_with_gst)
    context = {
        'category': category,
        'total_items_in_cart': total_items_in_cart,
        'cart': cart_items,
        'total_price': total_price,
        'user': request.user,
        'gst': gst,
        'total_price_with_gst': total_price_with_gst,

    }
    return render(request, 'index.html', context)



def shop(request, category=None):
    category = Category.objects.all()
    product = Product.objects.all()
    product_count = product.count()
    
    # Pagination
    paginator = Paginator(product, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Initialize cart-related variables
    cart_items = []
    total_items_in_cart = 0
    total_price = Decimal('0.00')
    gst = Decimal('0.00')
    total_price_with_gst = Decimal('0.00')

    if request.user.is_authenticated:
        # Retrieve cart items and calculate cart-related values if the user is authenticated
        cart_items = CartItem.objects.filter(cart__user=request.user)
        total_items_in_cart = cart_items.count()    
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        gst = total_price * Decimal('0.18')
        total_price_with_gst = total_price + gst
    
    price_range = request.GET.get('price_range')
    if price_range:
        price_range = price_range.split('-')
        product = Product.objects.filter(price__gte=price_range[0], price__lte=price_range[1])
        product_count = product.count()
        paginator = Paginator(product, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    category_name = request.GET.get('category')
    if category_name:
        product = Product.objects.filter(category__name=category_name)
        product_count = product.count()
        paginator = Paginator(product, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)    

    search_query = request.GET.get('q')
    if search_query:
        product = Product.objects.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        product_count = product.count()
        paginator = Paginator(product, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    context = {
        'total_items_in_cart': total_items_in_cart,
        'cart': cart_items,
        'total_price': total_price,
        'user': request.user,
        'gst': gst,
        'total_price_with_gst': total_price_with_gst,
        'category': category,
        'page_obj': page_obj,
        'product_count': product_count,
    }

    return render(request, 'shop.html', context)




def product_detail(request, name):
    # Original product
    pro = Product.objects.get(name=name)
    
    # Fetch related products (for example, products with the same category as the original product)
    related_products = Product.objects.filter(category=pro.category).exclude(name=name)[:4]  # Change this filter condition as per your related product logic
    
    context = {
        'pro': pro,
        'related_products': related_products,
    }

    return render(request, 'product_detail.html', context)




@login_required 
def addtocart(request, id):
    product = Product.objects.get(id=id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect(reverse('viewcart'))



def viewcart(request):
    cart_items = []
    total_items_in_cart = 0
    total_price = Decimal('0.00')
    gst = Decimal('0.00')
    total_price_with_gst = Decimal('0.00')

    if request.user.is_authenticated:
        # Retrieve cart items and calculate related values only if the user is authenticated
        cart_items = CartItem.objects.filter(cart__user=request.user)
        print(cart_items)
        total_items_in_cart = cart_items.count()    
        print(total_items_in_cart)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        print(total_price)
        gst = total_price * Decimal('0.18')
        print(gst)
        total_price_with_gst = total_price + gst
        print(total_price_with_gst)

    context = {
        'total_items_in_cart': total_items_in_cart,
        'cart': cart_items,
        'total_price': total_price,
        'user': request.user,
        'gst': gst,
        'total_price_with_gst': total_price_with_gst,
    }
    return render(request, 'viewcart.html', context)


@login_required
def removefromcart(request, id):
    cart_item = CartItem.objects.get(id=id)
    cart_item.delete()
    return redirect('viewcart')


def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if item.quantity < 5:
        item.quantity += 1
        item.save()
    return redirect('viewcart')

def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    return redirect('viewcart')



from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
from django.shortcuts import render, redirect
from .models import CartItem, BillingDetail, Order, OrderItem
from django.template.loader import render_to_string


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_price = Decimal(total_price)
    gst = total_price * Decimal('0.18')
    delivery_charge = Decimal('50.00')
    total_price_with_gst = total_price + delivery_charge + gst

    if request.method == "POST":
        # Extract form data
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        notes = request.POST.get('notes')
        address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')

        # Retrieve user and cart items
        user = request.user
        items = CartItem.objects.filter(cart__user=user)

        # Create billing details and order
        billing_details = BillingDetail.objects.create(
            first_name=f_name, last_name=l_name, email=email, phone=phone, 
            city=city, notes=notes, address=address, payment_method=payment_method
        )
        new_order = Order.objects.create(
            user=user, bil_detail=billing_details, total_amount=total_price_with_gst
        )

        # Create order items
        order_items = [OrderItem(order=new_order, product=item.product, quantity=item.quantity) for item in items]
        OrderItem.objects.bulk_create(order_items)

        # Clear the cart (delete all items in a single query)
        items.delete()

        # Send order confirmation email
        # Send order confirmation email with HTML content
        subject = 'Your Order Confirmation'
        html_message = render_to_string('order_email_template.html', {
            'user': user,
            'new_order': new_order,
            'total_price_with_gst': total_price_with_gst,
        })
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        try:
            send_mail(
                subject,
                message='',  # Empty string for plain text message since we have HTML content
                from_email=email_from,
                recipient_list=recipient_list,
                fail_silently=False,
                html_message=html_message,
            )

            # Add a success message to be displayed on the redirected page
            request.session['order_confirmation'] = True
            return redirect('index')
        except Exception as e:
            print(f"Error sending email: {e}")
            # You might want to log the error or handle it more appropriately
            return redirect('thankyou')  # Consider redire
    # Provide additional information in the context
    context = {
        'cart': cart_items,
        'total_price': total_price,
        'user': request.user,
        'gst': gst,
        'delivery_charge': delivery_charge,
        'total_price_with_gst': total_price_with_gst,
    }
    return render(request, 'checkout.html', context)


def thankyou(request):
    return render(request, 'thankyou.html')



def myorders(request):
    myorder = Order.objects.filter(user=request.user)
    myorderitems = OrderItem.objects.filter(order__user=request.user)
    cart_items = []
    total_items_in_cart = 0
    total_price = Decimal('0.00')
    gst = Decimal('0.00')
    total_price_with_gst = Decimal('0.00')

    if request.user.is_authenticated:
        # Retrieve cart items and calculate related values only if the user is authenticated
        cart_items = CartItem.objects.filter(cart__user=request.user)
        print(cart_items)
        total_items_in_cart = cart_items.count()    
        print(total_items_in_cart)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        print(total_price)
        gst = total_price * Decimal('0.18')
        print(gst)
        total_price_with_gst = total_price + gst
        print(total_price_with_gst)
    context = {
        'myorder': myorder,
        'myorderitems': myorderitems,
        'total_items_in_cart': total_items_in_cart,
        'cart': cart_items,
        'total_price': total_price,
        'user': request.user,
        'gst': gst,
        'total_price_with_gst': total_price_with_gst,
        
    }
    return render(request, 'myorders.html', context)



def contact(request):
    cart_items = []
    total_items_in_cart = 0
    total_price = Decimal('0.00')
    gst = Decimal('0.00')
    total_price_with_gst = Decimal('0.00')

    if request.user.is_authenticated:
        # Retrieve cart items and calculate related values only if the user is authenticated
        cart_items = CartItem.objects.filter(cart__user=request.user)
        print(cart_items)
        total_items_in_cart = cart_items.count()    
        print(total_items_in_cart)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        print(total_price)
        gst = total_price * Decimal('0.18')
        print(gst)
        total_price_with_gst = total_price + gst
        print(total_price_with_gst)
    context = {
        'total_items_in_cart': total_items_in_cart,
        'cart': cart_items,
        'total_price': total_price,
        'user': request.user,
        'gst': gst,
        'total_price_with_gst': total_price_with_gst,
        
    }
    
    return render(request, 'contact.html',context)

def about(request):
    cart_items = []
    total_items_in_cart = 0
    total_price = Decimal('0.00')
    gst = Decimal('0.00')
    total_price_with_gst = Decimal('0.00')

    if request.user.is_authenticated:
        # Retrieve cart items and calculate related values only if the user is authenticated
        cart_items = CartItem.objects.filter(cart__user=request.user)
        print(cart_items)
        total_items_in_cart = cart_items.count()    
        print(total_items_in_cart)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        print(total_price)
        gst = total_price * Decimal('0.18')
        print(gst)
        total_price_with_gst = total_price + gst
        print(total_price_with_gst)
    context = {
        'total_items_in_cart': total_items_in_cart,
        'cart': cart_items,
        'total_price': total_price,
        'user': request.user,
        'gst': gst,
        'total_price_with_gst': total_price_with_gst,
        
    }
    return render(request, 'about.html', context)

    # SIGNUP,LOGIN,LOGOUT


from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            # Add an error message to the messages framework
            messages.error(request, "Password and Confirm Password do not match.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('shop')  # Replace 'index' with your desired redirect URL after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logoutview(request):
    logout(request)
    return redirect('index')

