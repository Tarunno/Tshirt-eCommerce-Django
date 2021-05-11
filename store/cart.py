import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_total': 0, 'get_cart_total_item': 0}

    for i in cart:
        try:
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quentity'])

            order['get_cart_total_item'] += cart[i]['quentity']
            order['get_cart_total'] = total

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image': product.image
                },
                'quentity': cart[i]['quentity'],
                'get_total': total
            }
            items.append(item)
        except:
            pass
    return {'items': items, 'order': order}

def cartData(request):
    cookieData = cookieCart(request)
    order = cookieData['order']
    items = cookieData['items']
    return {'items': items, 'order': order}
