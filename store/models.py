from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    CATEGORY_CHOICES = [
        ('Laptop', 'Laptop'),
        ('Mobile', 'Mobile'),
        ('Headphone', 'Headphone'),
        ('Accessory', 'Accessory'),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='Laptop'
    )

    description = models.TextField()
    model_name = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='products/')
    discount = models.PositiveIntegerField(default=0)

    def average_rating(self):
        avg = self.review_set.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 5

    def discounted_price(self):
        return int(self.price - (self.price * self.discount / 100))

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="products/gallery/")

    def _str_(self):
        return f"{self.product.name} Image"

class ProductSpecification(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="specifications"
    )
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    def _str_(self):
        return f"{self.product.name} - {self.key}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Order(models.Model):
    user = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    amount = models.IntegerField(default=0)
    payment_method = models.CharField(max_length=50, default="COD")
    STATUS_CHOICES =[
        ("Ordered", "Ordered"),
        ("Packed", "Packed"),
        ("Shipped", "Shipped"),
        ("Out for Delivery", "Out for Delivary"),
        ("Delivered", "Delivered"),
    ]
    status = models.CharField(
        max_length=30,
        choices= STATUS_CHOICES,
        default="Ordered"
    )
    ordered_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, default="")
    mobile = models.CharField(max_length=15, default="")
    email = models.EmailField(default="")
    address = models.TextField(default="")
    city = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=100, default="")
    pincode = models.CharField(max_length=10, default="")

    def __str__(self):
        return self.product_name
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    
class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    def _str_(self):
        return self.code