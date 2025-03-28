from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.db.models import F, Sum
from .forms import UserRegisterForm,UserLoginForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 登録後に自動ログイン
            return redirect('product_list')  # トップページに移動
    else:
        form = UserRegisterForm()
    return render(request, 'shop/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserLoginForm()
    return render(request, 'shop/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity = F('quantity') + 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'shop/cart_detail.html', {'items': items, 'total': total})

@login_required
def create_order(request):
    items = CartItem.objects.filter(user=request.user)
    if not items.exists():
        return redirect('product_list')

    total_price = sum(item.product.price * item.quantity for item in items)
    order = Order.objects.create(user=request.user, total_price=total_price)

    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    items.delete()
    return render(request, 'shop/order_success.html', {'order': order})
