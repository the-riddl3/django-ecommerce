from django.db import models

from django.conf import settings

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField('products.Product', through='CartItem')

    def __str__(self):
        return "Cart id: %s" %(self.id)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    line_item_total = models.DecimalField(default=10.99, max_digits=100, decimal_places=2)
    notes = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def save(self, *args, **kwargs):
        # old line item total
        old_line_item_total = self.line_item_total

        # new line item total
        price = self.product.price
        self.line_item_total = price * self.quantity

        # update cart total
        if old_line_item_total and old_line_item_total != self.line_item_total:
            new_total = self.cart.total - old_line_item_total + self.line_item_total
            self.cart.total = new_total
            self.cart.save()

        # call the super method
        super(CartItem, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cart = self.cart
        line_item_total = self.line_item_total
        cart.total -= line_item_total
        cart.save()
        super(CartItem, self).delete(*args, **kwargs)

    def __str__(self):
        try:
            return str(self.cart.id)
        except:
            return self.product.title
