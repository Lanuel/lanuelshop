from django.shortcuts import render
from .models import Product


def index(request):
    """Return a webpage with a message."""
    products = Product.objects.all()
    return render(request, "index.html",{
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