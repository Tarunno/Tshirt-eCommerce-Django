from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
import json

from .models import *
from .forms import *
from .cart import cookieCart, cartData


def store(request):
    products = []
    categories = Category.objects.all()
    for category in categories:
        category_product = Product.objects.filter(category=category).all().order_by('-date')[0: 4]
        products.extend(category_product)

    on_sells = Product.objects.filter(on_sell=True).all()

    data = cartData(request)
    order = data['order']

    ratings = Rating.objects.all()

    context = {
        'order': order,
        'categories': categories,
        'products': products,
        'on_sells': on_sells,
        'title': 'Store',
    }
    return render(request, 'store/store.html', context)



def category_items(request, id):
    categories = Category.objects.all()
    if id == '-1':
        products = Product.objects.all().order_by('-date')
        category = "All"
    else:
        products = Product.objects.filter(category=id).all().order_by('-date')
        category = Category.objects.get(id=id)

    paginator = Paginator(products, 20)  # Show 20 product per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = cartData(request)
    order = data['order']

    context = {
        'order': order,
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

    data = cartData(request)
    order = data['order']

    context = {
        'order': order,
        'categories': categories,
        'products': page_obj,
        'title': 'Search',
    }
    return render(request, 'store/category.html', context)



def view_product(request, id):
    product = Product.objects.get(id=id)
    categories = Category.objects.all()
    data = cartData(request)
    order = data['order']

    ratings = Rating.objects.filter(product=product)
    sum_rated = ratings.count()
    sum_rating = sum([i.rating for i in ratings])

    if sum_rated == 0:
        rating = 0
    else:
        rating = sum_rating / sum_rated

    reviews = Review.objects.filter(product=product).all()

    context = {
        'product': product,
        'rating': rating,
        'rated': sum_rated,
        'reviews': reviews,
        'order': order,
        'categories': categories,
        'title': 'Product'
    }
    return render(request, 'store/product.html', context)



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



def cart(request):
    categories = Category.objects.all()
    data = cartData(request)
    order = data['order']
    items = data['items']

    context = {
        'order': order,
        'items': items,
        'categories': categories,
        'title': 'Cart'
    }
    return render(request, 'store/cart.html', context)



def checkout(request):
    categories = Category.objects.all()
    data = cartData(request)
    order = data['order']

    context = {
        'order': order,
        'categories': categories,
        'title': 'Checkout'
    }
    return render(request, 'store/checkout.html', context)

def order_placed(request):
    order = Order.objects.get(customer=request.user.customer)
    order.order_placed = True
    order.save()
    return JsonResponse("order placed", safe=False)

def about(request):
    categories = Category.objects.all()
    data = cartData(request)
    order = data['order']

    context = {
        'order': order,
        'categories': categories,
        'title': 'About'
    }
    return render(request, 'store/about.html', context)



def update_item(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productID)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem, created = OrderItem.objects.get_or_create(product=product, order=order)

    if action == 'add':
        orderitem.quentity = (orderitem.quentity + 1)
    elif action == 'remove':
        orderitem.quentity = (orderitem.quentity - 1)

    orderitem.save()
    messages.success(request, f'Product successfully added!')
    if orderitem.quentity <= 0:
        orderitem.delete()

    data = cartData(request)
    order = data['order']
    count = order.get_cart_total_item

    return JsonResponse({'quentity': count}, safe=False)



def signup(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name =request.POST.get('last_name')
        user = request.POST.get('username')
        email = request.POST.get('email')

        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=username)
            customer = Customer(user=user, email=email, name=first_name+" "+last_name+" "+username)
            customer.save()
            return redirect('login')
    else:
        form = UserRegistration()

    data = cartData(request)
    order = data['order']
    items = data['items']

    context = {
        'order': order,
        'title': 'Checkout',
        'form': form,
        'categories': categories,
        'title': 'signup'
    }
    return render(request, 'store/signup.html', context)
