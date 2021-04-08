def COD(request):
	order = Order.objects.get(user=self.request.user, ordered=False)
    
    order_items = order.items.all()
    order_items.update(ordered=True)
                
                
    for item in order_items:
        quantity = item.quantity 
        stock = item.item.stock 
        remaining = stock - quantity  
        item.item.stock = remaining  
                    
        item.item.save() 
        item.save()

        order.ordered = True
    
        order.ref_code = create_ref_code()
                
        order.save()


    messages.success(self.request, "Your order was successful")
    return redirect("/")
