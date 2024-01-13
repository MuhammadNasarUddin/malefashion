from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='static/category/', default='static/category/default.jpg')
    
        # Add other category-related fields as needed

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    # Add other product-related fields like sizes, colors, etc.

    def __str__(self):
        return f"{self.name} - {self.category.name}" 

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')


    def __str__(self):
        return f"Cart for {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Cart for {self.cart.user.username}"
   

class Order(models.Model):
    # Existing fields
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    bil_detail = models.ForeignKey('BillingDetail', on_delete=models.CASCADE, null=True, blank=True)
    
    
    def __str__(self):

        return f"Order #{self.id} by {self.user.username}"
    


class BillingDetail(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=100)
    notes = models.TextField()
    payment_method = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    # Add other fields related to an ordered item like price, discounts, etc.

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    



class User(models.Model):
    # Add fields for user like name, email, address, etc.
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)


    def __str__(self):
        return self.email    
    


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name   
    

