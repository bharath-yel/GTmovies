from django import template
register = template.Library()
@register.filter(name='get_quantity')
def get_cart_quantity(cart, movie_id):
    return int(cart[str(movie_id)])

@register.filter
def multiply(x, y):
    return x * y