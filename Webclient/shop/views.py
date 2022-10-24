import re
from django.shortcuts import redirect, render
from .models import *
from .form import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
import json
from django.http import  JsonResponse

# Create your views here.


def main(request):
    products = Product.objects.filter(trending=1)
    context = {'products': products}
    return render(request, 'shop/index.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)
            # nếu có người dùng cấp quyền đăng nhập vào và hiện thông báo
            if user is not None:
                auth.login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect("/")
            else:
                messages.error(request, "Invalid User Name or Password")
                return redirect("/login")
    return render(request, 'shop/login.html')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.success(request, "Logged out Successfully")
    return redirect("/")


def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Register success')
            return redirect('/login')
    return render(request, 'shop/register.html', {'form': form})


def collection(request):
    catagory = Catagory.objects.filter(status=0)
    context = {"catagory": catagory}
    return render(request, 'shop/collection.html', context)


def collectionview(request, name):
    # truy xuất loại hàng theo tên và status
    if Catagory.objects.filter(name=name, status=0):
        products = Product.objects.filter(category__name=name)
        context = {'products': products, "category_name": name}
        return render(request, 'products/product_index.html', context)
    else:
        messages.warning(request, "No such ... Found")
        return redirect('collection')


def product_detail(request, cname, pname):
    # truy xuất chi tiết mặt hàng
    if (Catagory.objects.filter(name=cname, status=0)):
        if (Product.objects.filter(name=pname, status=0)):
            products = Product.objects.filter(name=pname, status=0).first()
            return render(request, "products/product_detail.html", {"products": products})
        else:
            messages.error(request, "No Such Produtct Found")
            return redirect('collection')
    else:
        messages.error(request, "No Such Catagory Found")
        return redirect('collection')


def add_to_cart(request):
    if request.headers.get('x-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data['product_qty']
            product_id = data['pid']
            #print(request.user.id)
            product_status = Product.objects.get(id = product_id)
            
            if product_status:
                if Cart.objects.filter(user = request.user.id, product_id = product_id):
                    return JsonResponse({'status':'Product already in cart'}, status=200)
                else: 
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user = request.user, product_id = product_id, product_qty = product_qty)
                        return JsonResponse({'status':'Product added to cart'}, status = 200)
                    else:     
                        return JsonResponse({'status': 'Product stock not available'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)


def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user = request.user)
        context = {'cart': cart}
        return render(request, 'shop/cart.html', context)
    else:
        return redirect('/')
    

def remove_cart(request, id):
    #xóa theo id trả về trang tên cart
    cart_item = Cart.objects.filter(id = id)
    cart_item.delete()
    return redirect('/cart')

def check_out(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user = request.user)
        context = {'cart': cart}
        return render(request, 'shop/checkout.html', context)
    else:
        return redirect('/')




    