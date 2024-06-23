from carts.models import Cart, CartItem


class CartService:
    def __init__(self, user):
        self.user = user

    def get_cart(self):
        cart = Cart.objects.filter(user=self.user, active=True).first()
        if cart is None:
            cart = Cart.objects.create(user=self.user)
        return cart

    def remove_item(self, product):
        cart = self.get_cart()
        cart_item = cart.items.filter(product=product).first()
        if cart_item is not None:
            cart_item.delete()
        return cart_item

    def update_item(self, product, quantity):
        cart = self.get_cart()
        cart_item = cart.items.filter(product=product).first()
        if cart_item is not None:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity, line_item_total=product.price * quantity)
        return cart_item