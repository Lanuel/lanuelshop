from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm


def index(request):
    """Return a webpage with a message."""
    products = Product.objects.all()
    return render(request, "index.html", {
        "products": products
    })


def about(request):
    """Return a webpage under the index page with author's info."""
    return render(request, "about.html")


def contact(request):
    """Return a webpage under the index page with contact info."""
    return render(request, "contact.html")


def policy(request):
    """Return a webpage under the index page with privacy policy."""
    return render(request, "privacy.html")


def view_cart(request):
    cart = request.session.get('cart', {})

    total_price = 0
    for key, item in cart.items():  # ✅ Iterate properly
        item["total"] = round(float(item["price"]) * item["quantity"], 2)
        total_price += item["total"]

    # ✅ Save the updated cart back to session
    request.session["cart"] = cart
    request.session.modified = True  # ✅ Ensure session is saved

    return render(request, "cart.html",
                  {"cart": cart, "total_price": total_price})



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]["quantity"] += 1
    else:
        cart[str(product_id)] = {
            "name": product.name,
            "price": float(product.price),  # ✅ Convert Decimal to float
            "quantity": 1
        }

    request.session['cart'] = cart  # Save updated cart in session
    messages.success(request, f"✅ {product.name} added to cart!")
    return redirect('index')  # Ensure 'index' is named in urls.py


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        messages.success(request, "✅ Item removed from cart.")

    request.session["cart"] = cart
    return redirect("view_cart")


def increase_quantity(request, product_id):
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        cart[str(product_id)]["quantity"] += 1
        cart[str(product_id)]["total"] = round(
            cart[str(product_id)]["price"] * cart[str(product_id)]["quantity"],
            2)

    request.session["cart"] = cart
    request.session.modified = True
    messages.success(request, "✅ Item quantity updated.")

    return redirect("view_cart")


def decrease_quantity(request, product_id):
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        if cart[str(product_id)]["quantity"] > 1:
            cart[str(product_id)]["quantity"] -= 1
            cart[str(product_id)]["total"] = round(
                cart[str(product_id)]["price"] * cart[str(product_id)][
                    "quantity"], 2)
        else:
            del cart[str(product_id)]

    request.session["cart"] = cart
    request.session.modified = True
    messages.success(request, "✅ Item quantity updated.")

    return redirect("view_cart")


@login_required  # Ensures only logged-in users can access checkout
def checkout(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to proceed to checkout.")
        return redirect("login")  # Redirect to login page

    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect("index")  # Redirect to products page if cart is empty

    # Process checkout (e.g., save order to database)
    messages.success(request,
                     f"Order placed successfully! Confirmation sent to {request.user.email}")

    # Clear the cart after successful checkout
    request.session["cart"] = {}

    return redirect("index")  # Redirect to products page after checkout
# How would the message in the first condition be displayed when the user is
# immediately redirected to the login page?

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             "Account created successfully! "
                             "Please log in.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})
