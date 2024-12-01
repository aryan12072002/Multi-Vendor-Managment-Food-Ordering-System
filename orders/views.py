from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponse,JsonResponse
from marketplace.models import Cart,FoodItem
from .forms import orderform
from .models import Order,Payment,OrderedFood
import simplejson as json
from .utils import generate_order_number,order_total_by_vendor
from marketplace.context_processor import get_cart_amount
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from marketplace.models import Tax
import logging
from django.contrib.sites.shortcuts import get_current_site
@login_required(login_url='login')
def place_order(request):
    cart_items=Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count=cart_items.count()
    if cart_count<=0:
        return redirect('marketplace')
    
    vendors_ids=[]
    for i in cart_items:
        if i.fooditem.vendor.id not in vendors_ids:
            vendors_ids.append(i.fooditem.vendor.id)
    #{'vendor_id':{'subtotal':{'tax_type':{'tax_percentage':'tax_amount'}}}}       
    get_tax=Tax.objects.filter(is_active=True)
    subtotal=0
    total_data={}
    k={}
    for i in cart_items:
        fooditem=FoodItem.objects.get(pk=i.fooditem.id,vendor_id__in=vendors_ids)
        v_id=fooditem.vendor.id
        if v_id in k:
            subtotal=k[v_id]
            subtotal+=(fooditem.price*i.quantity)
            k[v_id]=subtotal
        else:
            subtotal=(fooditem.price*i.quantity)
            k[v_id]=subtotal
        print(k)
        #calculate tax_data
        tax_dict={}
        for i in get_tax:
            tax_type=i.tax_type
            tax_percentage=i.tax_percentage
            tax_amount=round((tax_percentage*subtotal)/100,2)
            tax_dict.update({tax_type:{str(tax_percentage):str(tax_amount)}})
        #construct total data
        total_data.update({fooditem.vendor.id:{str(subtotal):str(tax_dict)}})
        print(total_data)
        print(tax_dict)
        
        print(fooditem,fooditem.vendor.id)
    
    
    subtotal=get_cart_amount(request)['subtotal']
    total_tax=get_cart_amount(request)['tax']
    grand_total=get_cart_amount(request)['grand_total']
    tax_data=get_cart_amount(request)['tax_dict'] #{'tax':{'cgst':30,'sgst':12}}
    if request.method=='POST':
        form=orderform(request.POST)
        if form.is_valid():
            order=Order()
            order.first_name=form.cleaned_data['first_name']
            order.last_name=form.cleaned_data['last_name']
            order.phone=form.cleaned_data['phone']
            order.email=form.cleaned_data['email']
            order.address=form.cleaned_data['address']
            order.country=form.cleaned_data['country']
            order.state=form.cleaned_data['state']
            order.city=form.cleaned_data['city']
            order.pin_code=form.cleaned_data['pin_code']
            order.user=request.user
            order.total=grand_total
            order.tax_data=json.dumps(tax_data)
            order.total_data=json.dumps(total_data)
            order.total_tax=total_tax
            order.payment_method=request.POST['payment_method']
            order.save() #order id pk is generated
            order.order_number=generate_order_number(order.id)
            order.vendors.add(*vendors_ids)
            order.save()
            context={
                'order':order,
                'cart_items':cart_items
            }
            
            return render(request,'orders/place_order.html',context)
        else:
            print(form.errors)
    else:
        form=orderform()
        
    return  render(request,'orders/place_order.html')
@login_required(login_url='login')
def payments(request):
    #check if the request is ajax or not
    if request.headers.get("x-requested-with")=='XMLHttpRequest' and request.method=='POST':
        order_number=request.POST.get('order_number')
        transaction_id=request.POST.get('transaction_id')
        payment_method=request.POST.get('payment_method')
        status=request.POST.get('status')
        print(order_number,transaction_id,payment_method,status)
        order=Order.objects.get(user=request.user,order_number=order_number)
        payment=Payment(
            user=request.user,
            transaction_id=transaction_id,
            payment_method=payment_method,
            amount=order.total,
            status=status
        )
        payment.save()
        #store the payment details in the payment model
        order.payment=payment
        order.is_ordered=True
        order.save()
        # move the cart items to ordered food model
        cart_items=Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food=OrderedFood()
            ordered_food.order=order
            ordered_food.payment=payment
            ordered_food.user=request.user
            ordered_food.fooditem=item.fooditem
            ordered_food.quantity=item.quantity
            ordered_food.price=item.fooditem.price
            ordered_food.amount=item.fooditem.price*item.quantity
            ordered_food.save()
        
        #send order confirmation email to the customer
        mail_subject='Thank you for the customer'
        mail_template='orders/order_confirmation_email.html'
        ordered_food= OrderedFood.objects.filter(order=order)
        customer_subtotal= 0
        for item in ordered_food:
            customer_subtotal +=(item.price * item.quantity)
        tax_data= json.loads(order.tax_data)
        context={
            'user':request.user,
            'order':order, 
            'to_email':order.email,
            'ordered_food':ordered_food,
            'domain':get_current_site(request),
            'customer_subtotal':customer_subtotal,
            'tax_data':tax_data,
            
        }
            
        send_notification(mail_subject,mail_template,context)
        
        #send order received mail to the vendor
        mail_subject='You have received a new order'
        mail_template='orders/new_order_received.html'
        to_emails=[]
        for i in cart_items:
            if i.fooditem.vendor.user.email not in to_emails:
                to_emails.append(i.fooditem.vendor.user.email)
                ordered_food_to_vendor = OrderedFood.objects.filter(order=order,fooditem__vendor=i.fooditem.vendor)
                print(ordered_food_to_vendor)
       
        context={
            'order':order,
            'to_email':to_emails,
            'ordered_food_to_vendor':ordered_food_to_vendor,
            'vendor_subtotal':order_total_by_vendor(order, i.fooditem.vendor.id)['subtotal'],
            'tax_data':order_total_by_vendor(order, i.fooditem.vendor.id)['tax_dict'],
            'vendor_grand_total':order_total_by_vendor(order, i.fooditem.vendor.id)['grand_total'],
        }
        
        send_notification(mail_subject,mail_template,context)
    
        #clear the cart if the payment is success
        cart_items.delete()
        #return HttpResponse("Data saved and email sent")
        
        #return back to ajax the status success of failures.
        
        response={
            'order_number':order_number,
            'transaction_id':transaction_id
        }
        return JsonResponse(response)
    return HttpResponse('Payments view')
def order_complete(request):
    # Initialize logger
    logger = logging.getLogger(__name__)
    order_number=request.GET.get('order_number')
    transaction_id=request.GET.get('transaction_id')
    try:
        order=Order.objects.get(order_number=order_number,payment__transaction_id=transaction_id,is_ordered=True)
        ordered_food=OrderedFood.objects.filter(order=order)
        subtotal=0
        for item in ordered_food:
            subtotal+=(item.price*item.quantity)
        tax_data=order.tax_data
        context={
                'order':order,
                'ordered_food':ordered_food,
                'subtotal':subtotal,
                'tax_data':tax_data,
        }
        return render(request,'orders/order_complete.html',context)
    except ObjectDoesNotExist:
        logger.warning(f"Order not found for user {request.user} with order_no {order_number} and trans_id {transaction_id}")
        return redirect('home')


        
    