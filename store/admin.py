from django.contrib import admin
from .models import Product, Cart, Order, Wishlist, Review, Coupon, ProductImage, ProductSpecification

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'price',
    )

    search_fields = (
        'category',
        'name',
    )

    list_filter = (
        'price',
    )

    inlines = [
        ProductImageInline,
        ProductSpecificationInline,
        ]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'quantity',
    )

    search_fields = (
        'product__name',
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'product_name',
        'amount',
        'payment_method',
        'status',
        'ordered_at',
    )
    list_filter =(
        'status',
        'payment_method',
        'ordered_at',
    )
    search_fields =(
        'user',
        'product_name',
    )


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'product',
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'user',
        'rating',
        'created_at',
    )

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display =("code", "discount", "active")

