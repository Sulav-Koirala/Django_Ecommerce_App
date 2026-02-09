from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Product,Order,OrderItem

def home(request):
    isadminuser = False
    if request.user.is_authenticated:
        isadminuser = request.user.is_superuser
    context = {
        "isadminuser" : isadminuser
    }
    return render(request,'store/home.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            return render(request, 'store/register.html',{'error': 'email already exists'})
        else:
            User.objects.create_user(username=username,email=email, password=password)
            return redirect('store:login')
    return render(request, 'store/register.html')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect('store:home')
            else :
                return render(request,'store/login.html',{'error' : 'Invalid credentials'})
        except User.DoesNotExist:
            return render(request, 'store/login.html', {'error': 'User with this email does not exist'})
    return render(request, 'store/login.html')

def logout_user(request):
    logout(request)
    return redirect('store:login')

def get_cart(request):
    cart = request.session.get('cart', {})
    data = []
    total = 0
    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        data.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'cart_quantity': qty
        })
        total += product.price * qty
    return JsonResponse({'items': data, 'total': total})

def add_to_cart(request,product_id):
    cart = request.session.get('cart', {})
    id = str(product_id)
    if id in cart:
        cart[id] += 1
    else:
        cart[id] = 1
    request.session['cart'] = cart
    request.session.modified = True
    product = Product.objects.get(id=product_id)
    total = 0
    for pid, qty in cart.items():
        p=Product.objects.get(id=pid)
        total += p.price * qty
    return JsonResponse({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'cart_quantity': cart[id],
        'total': float(total)
    })

def delete_from_cart(request,product_id):
    cart = request.session.get('cart' , {})
    id = str(product_id)
    if id in cart:
        del cart[id]
    request.session['cart'] = cart
    request.session.modified = True
    total=0
    for pid,qty in cart.items():
        p = Product.objects.get(id = pid)
        total += p.price * qty
    return JsonResponse({
        'removed_id' : product_id,
        'total' : float(total)
    })

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return JsonResponse({'error': 'Cart is empty'}, status=400)
    total = 0
    order = Order.objects.create(user=request.user, total_price=0)
    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        OrderItem.objects.create(
            order = order,
            product = product,
            quantity = qty,
            price = product.price
        )
        total += product.price * qty
    order.total_price = total
    order.save()
    request.session['cart'] = {}
    request.session.modified = True
    return JsonResponse({'success': True,'order_id': order.id})