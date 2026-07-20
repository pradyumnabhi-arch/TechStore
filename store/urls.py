from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('product/<int:id>/', views.product_detail, name='product_detail'),

    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart_view, name='cart'),

    path('increase_quantity/<int:id>/', views.increase_quantity, name='increase_quantity'),

    path('decrease_quantity/<int:id>/', views.decrease_quantity, name='decrease_quantity'),

    path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),

    path('register/', views.register, name='register'),

    path('login/', views.user_login, name='login'),

    path('logout/', views.user_logout, name='logout'),

    path('checkout/', views.checkout, name='checkout'),

    path('place_order/', views.place_order, name='place_order'),

    path('order-history/', views.order_history, name='order_history'),

    path('wishlist/', views.wishlist_view, name='wishlist'),

    path('add_to_wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),

    path('remove_from_wishlist/<int:id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    path('search/', views.search, name='search'),

    path('add_review/<int:id>/', views.add_review, name='add_review'),

    path('signup/', views.signup, name='signup'),

    path('payment/', views.payment, name='payment'),

    path('payment_success/', views.payment_success, name='payment_success'),

    path('invoice/<int:id>/', views.invoice, name='invoice'),

    path('profile/', views.profile, name='profile'),

    path('track-order/<int:id>/', views.track_order, name='track_order'),
]