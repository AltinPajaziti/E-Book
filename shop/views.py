from django.shortcuts import render
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from .models import Product , Order , OrderProduct , Slide
from django.contrib.auth.decorators import login_required , permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User

from cart.cart import Cart
from .forms import ProductForm



@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_detail(request):
    cart = Cart(request)
    cart_items = cart.cart.values()
    print(cart_items)  # Add this line to check the content of cart_items
    total_price = sum(item['quantity'] * float(item['price']) for item in cart_items) 
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)


@login_required(login_url="/users/login")
def checkout(request):
    return render(request, 'checkout.html')

def cart(request):
    return render(request, 'cart.html')
#-----auth
@login_required(login_url='/auth/login')
@permission_required('order.delete_order', raise_exception=True)
def delete_order(request, id):
    Order.objects.filter(id=id).delete()
    return redirect('dashboard')
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    context = {
        'form': form
    }

    return render(request, 'registration/register.html', context)


def logout_user(request):
    logout(request)
    return redirect('index')



# def index(request):
#     products = Product.objects.order_by('-id')[:4]
#     slides = Slide.objects.order_by('-id')[:3]
#     context = {
#         'slides': slides,
#         'products': products
#     }
#     render(request ,'layouts/app.html' , context)
#     return render(request, 'index.html', context)

def index(request):
    header_products = Product.objects.all()[:6] 
    
    rare_books = Product.objects.all()[:3]  
    
    latest_products = Product.objects.all()[15:19]
    footer = Product.objects.all()[11:13] 
    
    context = {
        'header_products': header_products,
        'rare_books': rare_books,
        'latest_products': latest_products,
        'footer': footer,
    }
    render(request ,'layouts/app.html' , context)
    return render(request, 'index.html', context)


def checkout(request):
    if request.method == 'POST':
        if request.session.get('cart'):
            data = request.POST
            total = 0.0
            description = f"{data['fullname']} <br /> {data['email']} <br /> {data['phone']} <br /> {data['address']}"

            for pid, item in request.session.get('cart').items():
                total += (float(item['price']) * int(item['quantity']))

            order = Order.objects.create(user=User.objects.get(id=request.user.id), description=description, total=total)

            for pid, item in request.session.get('cart').items():
                OrderProduct.objects.create(order=Order.objects.latest('id'), product=Product.objects.get(id=item['product_id']))

            del(request.session['cart'])
            return redirect('index')
        else:
            return redirect('cart')
    
    return redirect('cart_detail')

def search(request):
    if request.method == 'POST':
        if len(request.POST['query']) > 0:
            return redirect('shop', q=request.POST['query'])
        
    return redirect('shop', q='')

def filter(request):
    if request.method == 'POST':
        if request.POST['filter'] == 'price_asc':
            products = Product.objects.order_by('price')
        
        if request.POST['filter'] == 'price_desc':
            products = Product.objects.order_by('-price')

        return render(request, 'shop.html', {'products' : products})
        
    return redirect('shop', q='')

def shop(request, q=None):
    products = Product.objects.all()
    
    if q is not None:
        products = products.filter(name__contains=q).order_by('-id')
    
    
    products = products[:20]

    context = {
        'products': products
    }
    return render(request, 'shop.html', context)


def view_product(request, id):
    product = Product.objects.filter(id=id).first()
    context = {
        'product': product
    }
    return render(request, 'view-product.html', context)

@login_required(login_url='/auth/login')
def dashboard(request):
    user_groups = request.user.groups.values_list('name',flat = True)
    products = Product.objects.count()

    if('admin' in user_groups):
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user_id=request.user.id)

    context = {
        'products': products,
        'orders': orders
    }

    return render(request, 'dashboard/index.html', context)