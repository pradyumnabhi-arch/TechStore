from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, Order, Wishlist, Review, ProductImage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator

def home(request):
    category = request.GET.get('category')
    sort = request.GET.get('sort')
    search = request.GET.get('search')

    products = Product.objects.all()

    if search:
        products = products.filter(name__icontains=search)

    if category:
        products = products.filter(category=category)

    if sort == "low":
        products = products.order_by('price')
    elif sort == "high":
        products = products.order_by('-price')

        paginator = Paginator(products, 8) #8 product per page
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)

    return render(request, 'store/home.html', {
        'products': products
    })


# Product Detail
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    product_images = ProductImage.objects.filter(product=product)

    reviews = Review.objects.filter(product=product)

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    return render(request, "store/product_detail.html", {
        "product": product,
        "product_images": product_images,
        "reviews": reviews,
        "related_products": related_products,
    })

def add_review(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        rating = request.POST['rating']
        comment = request.POST['comment']

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )

    return redirect('product_detail', id=id)


# Add to Cart
def add_to_cart(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    product = get_object_or_404(Product, id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )
    if cart_item.quantity >= product.stock:
        messages.warning(request, "No more stock available!")
        return redirect('home')

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


# Cart
def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = Cart.objects.filter(user=request.user)

    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# Increase Quantity
def increase_quantity(request, id):
    cart_item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')


# Decrease Quantity
def decrease_quantity(request, id):
    cart_item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


# Remove Item
def remove_from_cart(request, id):
    cart_item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    cart_item.delete()

    return redirect('cart')


# Register
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(request, "Account created successfully.")
        return redirect("login")

    return render(request, "store/register.html")


# Login
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("home")

        messages.error(request, "Invalid username or password.")

    return render(request, "store/login.html")


# Logout
def user_logout(request):
    logout(request)
    return redirect("home")

# Checkout
def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    discount = 0
    coupon_message = ""

    if request.method == "POST":
        coupon = request.POST.get("coupon", "").strip().upper()

        if coupon == "SAVE10":
            discount = total * 10 // 100
            coupon_message = "Coupon Applied Successfully! 🎉"

        elif coupon == "TECH20":
            discount = total * 20 // 100
            coupon_message = "Coupon Applied Successfully! 🎉"

        elif coupon:
            coupon_message = "Invalid Coupon Code ❌"

        total -= discount

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        'coupon_message': coupon_message,
    })


# Place Order
def place_order(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    for item in cart_items:
        Order.objects.create(
            user=request.user.username,
            product_name=item.product.name,
            amount=item.product.price * item.quantity,
            payment_method="COD"
        )

    cart_items.delete()

    return render(request, 'store/order_success.html')


# Order History
def order_history(request):
    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(user=request.user.username).order_by('-ordered_at')

    return render(request, 'store/order_history.html', {
        'orders': orders
    })

def add_to_wishlist(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    product = get_object_or_404(Product, id=id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('home')


def wishlist_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    wishlist_items = Wishlist.objects.filter(user=request.user)

    return render(request, 'store/wishlist.html', {
        'wishlist_items': wishlist_items
    })


def remove_from_wishlist(request, id):
    item = get_object_or_404(
        Wishlist,
        id=id,
        user=request.user
    )

    item.delete()

    return redirect('wishlist')

def search(request):
    query = request.GET.get('q')

    products = Product.objects.all()

    if query:
        products = Product.objects.filter(
            name__icontains=query
        )

    return render(request, 'store/search.html', {
        'products': products,
        'query': query
    })

def signup(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm_password']

        if password != confirm:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        messages.success(request, "Welcome to TechStore!")

        return redirect('home')

    return render(request, 'store/signup.html')

def payment(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method != "POST":
        return redirect('checkout')
    
    context ={
        "name": request.POST.get("name"),
        "mobile": request.POST.get("mobile"),
        "email": request.POST.get("email"),
        "address": request.POST.get("address"),
        "city": request.POST.get("city"),
        "state": request.POST.get("state"),
        "pincode": request.POST.get("pincode")
    }

    return render(request, "store/payment.html", context)


def payment_success(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart')

    last_order = None

    for item in cart_items:
        last_order = Order.objects.create(
            user=request.user.username,
            product_name=item.product.name,
            amount=int(item.product.price * item.quantity),
            payment_method=request.POST.get("payment", "UPI"),

            name=request.POST.get("name"),
            mobile=request.POST.get("mobile"),
            email=request.POST.get("email"),
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            state=request.POST.get("state"),
            pincode=request.POST.get("pincode")
            #item.product.stock -= item.quantity item.product.save()
        )

    cart_items.delete()

    request.session.pop("name", None)
    request.session.pop("mobile", None)
    request.session.pop("address", None)
    request.session.pop("city", None)
    request.session.pop("state", None)
    request.session.pop("pincode", None)

    return redirect("invoice", id=last_order.id)

def invoice(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    order = get_object_or_404(
        Order,
        id=id,
        user=request.user.username
    )

    return render(request, 'store/invoice.html', {
        'order': order
    })

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'store/profile.html')

def track_order(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    order = get_object_or_404(
        Order,
        id=id,
        user=request.user.username
    )

    return render(request, 'store/track_order.html', {
        'order': order
    })