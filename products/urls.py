from . import views
from django.urls import path
from .views import add_to_cart, remove_from_cart, checkout
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("privacy-policy/", views.policy, name="policy"),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path("products/", views.index, name="products"),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart,
         name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path("cart/decrease/<int:product_id>/", views.decrease_quantity,
         name="decrease_quantity"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart,
         name="remove_from_cart"),
    path("cart/increase/<int:product_id>/", views.increase_quantity,
         name="increase_quantity"),


    # Authentication
    path("login/", auth_views.LoginView.as_view(template_name="login.html"),
         name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
]
