order = Order.objects.get(user=request.user, ordered=False)
atam = OrderItem.objects.filter(
    user=request.user,
    ordered=False
)
if atam.exists():
    item = atam[0]
    order.item = item
    order.save()
