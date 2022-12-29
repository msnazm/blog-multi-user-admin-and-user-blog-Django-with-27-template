from main.models import Store


def allstores(request):
    from .models import OrderItem,Order
    from django.contrib.auth.models import User
    sum_orders = 0
    if request.user.id:
        order_filter = Order.objects.filter(user_id=request.user.id,isfinal=False)
        if order_filter:
            sum_orders = OrderItem.objects.filter(user_id = request.user.id,isfinal=False).count()
    if request.user.id and request.user.is_user_store == 1:
       store = Store.objects.get(pk = request.user.store_id)
    else:
        store = 0
    return {'sum_orders':sum_orders,'store':store}
