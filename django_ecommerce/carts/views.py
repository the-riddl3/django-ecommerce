from django.shortcuts import redirect, render

from carts.models import Cart
from carts.schemas import DeleteCartSchema, UpdateCartSchema
from carts.services.cart_service import CartService
from products.models import Product

# Create your views here.
def index(request):
    return render(request, "carts/index.html", {})


def update(request):
    try:
        UpdateCartSchema().model_validate(request.POST.dict())
        product_id = request.POST.get('product_id')
        product_obj = Product.objects.get(id=product_id)
        quantity = request.POST.get('quantity')
        user = request.user
        CartService(user).update_item(product_obj, quantity)
    except:
        pass
    return redirect("carts:index")


def delete(request):
    try:
        DeleteCartSchema().model_validate(request.POST.dict())
        product_id = request.POST.get('product_id')
        product_obj = Product.objects.get(id=product_id)
        user = request.user
        CartService(user).remove_item(product_obj)
    except:
        pass
    return redirect("carts:index")
