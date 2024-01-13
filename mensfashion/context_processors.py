from .models import CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user=request.user)
        total_items_in_cart = cart_items.count()
    else:
        total_items_in_cart = 0
    
    return {'total_items_in_cart': total_items_in_cart}