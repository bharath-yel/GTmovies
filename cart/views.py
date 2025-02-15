from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item, Cart, CartItem
from django.contrib.auth.decorators import login_required

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids == []):
        return redirect('cart.index')
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()
    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
    request.session['cart'] = {}
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    return render(request, 'cart/purchase.html',
        {'template_data': template_data})
def index(request):
    cart_total = 0
    movies_in_cart = []

    if request.user.is_authenticated:
      cart, created = Cart.objects.get_or_create(user=request.user)
      cart_items = CartItem.objects.filter(cart=cart)
      movies_in_cart = [(item.movie, item.quantity) for item in cart_items]
      cart_total = sum(item[0].price * item[1] for item in movies_in_cart)
    else:
        cart = request.session.get('cart', {})
        movie_ids = list(cart.keys())
        for movie_id in movie_ids:
            movie = Movie.objects.get(id=movie_id)
            quantity = cart[movie_id]
            movies_in_cart.append((movie, quantity))
        cart_total = sum(item[0].price * item[1] for item in movies_in_cart)

    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html',
                {'template_data': template_data})
def add(request, id):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user) # need to create Cart model
        movie = get_object_or_404(Movie, id=id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, movie=movie)
        if not created:
            cart_item.quantity += int(request.POST.get('quantity', 1))
        cart_item.save()

        return redirect('cart.index')
    else: # user is not logged in
        cart = request.session.get('cart', {})
        new_quantity = int(request.POST.get('quantity', 1))
        if str(id) in cart:
            cart[str(id)] += new_quantity
        else:
            cart[str(id)] = new_quantity
        request.session['cart'] = cart
        return redirect('cart.index')

def remove(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        if cart[str(id)] > 1:
            cart[str(id)] -= 1
        else:
            del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart.index')

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')