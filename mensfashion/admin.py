from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Cart, CartItem, User, Contact,BillingDetail


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(User)
admin.site.register(Contact)
admin.site.register(BillingDetail)