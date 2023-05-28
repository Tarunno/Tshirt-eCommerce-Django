from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
import sys

from .models import *
from .forms import *
from .cart import cookieCart, cartData


def store(request):
    products = []
    categories = Category.objects.all()
    for category in categories:
        category_product = Product.objects.filter(category=category).all().order_by('-date')[0: 4]
        products.extend(category_product)

    on_sells = Product.objects.filter(on_sell=True).all().order_by('-date')

    data = cookieCart(request)
    cart_info = data['order']

    ratings = Rating.objects.all()

    context = {
        'categories': categories,
        'products': products,
        'on_sells': on_sells,
        'title': 'Store',
        'cart_info': cart_info
    }
    return render(request, 'store/store.html', context)


def category_items(request, id):
    categories = Category.objects.all()
    products = Product.objects.all().order_by('-date')

    if request.method == 'POST':
        starting_price = 0
        ending_price = sys.maxsize

        category = request.POST.get('category')
        color = request.POST.get('colors')
        size = request.POST.get('sizes')
        starting_price = request.POST.get('starting-price')
        if starting_price: float(starting_price)
        ending_price = request.POST.get('ending-price')
        if starting_price: float(starting_price)
        on_sell = request.POST.get('on-sell')
        free_delivery = request.POST.get('free-delivery')
        on_stock = request.POST.get('on-stock')

        if starting_price or ending_price:
            products = Product.objects.filter(price__gte=starting_price, price__lte=ending_price)

        if category:
            category = Category.objects.get(name=category)
            products  = products.filter(category=category)
        if color:
            products = products.filter(color=color)
        if size:
            products = products.filter(size=size)
        if on_sell:
            products = products.filter(on_sell=True)
        if free_delivery:
            products = products.filter(delivery=True)
        if on_stock:
            products = products.filter(on_stock=True)


    else:
        if id == '-1':
            products = Product.objects.all().order_by('-date')
            category = "All"
        else:
            products = Product.objects.filter(category=id).all().order_by('-date')
            category = Category.objects.get(id=id)

    paginator = Paginator(products, 20)  # Show 20 product per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = cookieCart(request)
    cart_info = data['order']

    context = {
        'cart_info': cart_info,
        'categories': categories,
        'products': page_obj,
        'title': category,
    }
    return render(request, 'store/category.html', context)



def search(request, query):
    queries = query.split(' ')

    products = Product.objects.all().filter(name__icontains=query)

    if len(queries) > 1:
        for i in queries:
            if i == "Shirt" or i == "shirt" or i == "Tshirt" or i == "tshirt":
                continue
            product = Product.objects.all().filter(name__icontains=i)
            products |= product

    products = products.distinct().order_by('-date')

    categories = Category.objects.all()

    paginator = Paginator(products, 20)  # Show 20 product per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = cookieCart(request)
    cart_info = data['order']

    context = {
        'cart_info': cart_info,
        'categories': categories,
        'products': page_obj,
        'title': 'Search',
    }
    return render(request, 'store/category.html', context)


def view_product(request, id):
    product = Product.objects.get(id=id)
    categories = Category.objects.all()

    ratings = Rating.objects.filter(product=product)
    sum_rated = ratings.count()
    sum_rating = sum([i.rating for i in ratings])

    if sum_rated == 0:
        rating = 0
    else:
        rating = sum_rating / sum_rated

    reviews = Review.objects.filter(product=product).all()
    data = cookieCart(request)
    cart_info = data['order']

    context = {
        'cart_info': cart_info,
        'product': product,
        'rating': rating,
        'rated': sum_rated,
        'reviews': reviews,
        'categories': categories,
        'title': 'Product'
    }
    return render(request, 'store/product.html', context)


@login_required(login_url="login")
def rating_update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = data['user']
        productID = data['productID']
        product = Product.objects.get(id=productID)
        user = User.objects.get(id=user)
        rating = int(data['rating'])
        if Rating.objects.filter(user=user, product=product).exists() > 0:
            rated = Rating.objects.get(user=user, product=product)
            rated.rating = rating
            rated.save()
        else:
            rated, created = Rating.objects.get_or_create(user=user, product=product, rating=rating)
            rated.save()
        ratings = Rating.objects.filter(product=product)
        sum_rated = ratings.count()
        sum_rating = sum([i.rating for i in ratings])
        if sum_rated == 0:
            total_rating = 0
        else:
            total_rating = sum_rating/ sum_rated

    return JsonResponse({'total_rating': total_rating}, safe=False)


@login_required(login_url="login")
def update_review(request):
    data = json.loads(request.body)
    product = Product.objects.get(id=data['productID'])
    user = request.user
    action = data['action']

    if action == "add":
        review = data['review']
        reviewed, created = Review.objects.get_or_create(user=user, product=product, review=review)
        reviewed.save()
        return JsonResponse({'status': 'added'})
    else:
        reviewID = data['reviewID']
        review = Review.objects.get(id=reviewID)
        review.delete()
        return JsonResponse({'status': 'deleted'})


@login_required(login_url="login")
def cart(request, action):
    categories = Category.objects.all()
    data = cookieCart(request)
    order, created = Order.objects.get_or_create(customer=request.user.customer)
    if action == "none":
        items = data['items']
        cart_info = data['order']
    elif action == 'redirect':
        items = []
        cart_info = {'get_cart_total': 0, 'get_cart_total_item': 0}

    context = {
        'order': order,
        'cart_info': cart_info,
        'items': items,
        'categories': categories,
        'title': 'Cart'
    }
    return render(request, 'store/cart.html', context)

@login_required(login_url="login")
def checkout(request):
    categories = Category.objects.all()
    data = cookieCart(request)
    cart_info = data['order']

    context = {
        'cart_info': cart_info,
        'categories': categories,
        'title': 'Checkout'
    }
    return render(request, 'store/checkout.html', context)

@login_required(login_url="login")
def order_placed(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart_data = cartData(request)
        order, created = Order.objects.get_or_create(customer=request.user.customer)
        Shipping.objects.create(customer=request.user.customer,
                                order=order, address=data['address'],
                                city=data['city'],
                                state=data['state'],
                                zip=data['zip'])
        for i in cart_data['items']:
            product = Product.objects.get(id=i['product']['id'])
            OrderItem.objects.create(product=product, order=order, quentity=i['quentity'])
        order = Order.objects.get(customer=request.user.customer)
        order.order_placed = True
        order.complete = False
        order.save()
        return redirect('cart', 'redirect')


def about(request):
    categories = Category.objects.all()
    data = cookieCart(request)
    cart_info = data['order']

    context = {
        'cart_info': cart_info,
        'categories': categories,
        'title': 'About'
    }
    return render(request, 'store/about.html', context)


def signup(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name =request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')

        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistration()

    data = cookieCart(request)
    cart_info = data['order']

    context = {
        'cart_info': cart_info,
        'title': 'Checkout',
        'form': form,
        'categories': categories,
        'title': 'signup'
    }
    return render(request, 'store/signup.html', context)


@login_required(login_url="login")
def custom(request):
    categories = Category.objects.all()
    data = cookieCart(request)
    cart_info = data['order']

    if request.method == 'POST':
        form = CustomTshirtForm(request.POST, request.FILES)
        if form.is_valid():
            order, created = Order.objects.get_or_create(customer=request.user.customer)
            order.custom = True
            order.order_placed = True
            order.save()

            form = form.save(commit=False)
            form.customer = request.user.customer
            form.order = order
            form.save()

    context = {
        'categories': categories,
        'cart_info': cart_info,
        'title': 'Custom'
    }
    return render(request, 'store/custom.html', context)
