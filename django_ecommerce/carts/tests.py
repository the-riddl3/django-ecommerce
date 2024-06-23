from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from products.models import Product
from carts.models import Cart, CartItem

class CartTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'email@email.com', 'password')
        self.client.login(username='testuser', password='password')
        self.product = Product.objects.create(name='product', price=100)
    
    def test_add_to_cart(self):
        response = self.client.post(reverse('carts:update'), {'product_id': self.product.id, 'quantity': 2})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(CartItem.objects.count(), 1)
        cart = Cart.objects.first()
        cart_item = CartItem.objects.first()
        self.assertEqual(cart.total, 200)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.line_item_total, 200)

    def test_update_quantity(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        response = self.client.post(reverse('carts:update'), {'product_id': self.product.id, 'quantity': 3})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(CartItem.objects.count(), 1)
        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.quantity, 3)
        self.assertEqual(cart_item.line_item_total, 300)
        self.assertEqual(cart.total, 300)
    
    def test_remove_from_cart(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product)
        response = self.client.post(reverse('carts:delete'), {'product_id': self.product.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(CartItem.objects.count(), 0)
        self.assertEqual(cart.total, 0)