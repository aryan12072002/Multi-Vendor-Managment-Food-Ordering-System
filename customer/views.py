from django.shortcuts import render, get_object_or_404,redirect
from accounts.models import UserProfile,User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import Userinfoform,UserProfileForm
from orders.models import Order,OrderedFood
from django.core.exceptions import ObjectDoesNotExist
import logging
import json
@login_required(login_url='login')
def cprofile(request):
    profile=get_object_or_404(UserProfile,user=request.user)
    if request.method=='POST':
        profile_form=UserProfileForm(request.POST,request.FILES,instance=profile)
        user_form=Userinfoform(request.POST,instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request,'Profile updated')
            return redirect('cprofile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form=UserProfileForm(instance=profile)
        user_form=Userinfoform(instance=request.user)
    context={
        'profile_form':profile_form,
        'user_form':user_form,
        'profile':profile,
    }
    return render(request,'customer/cprofile.html',context)
def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    
    context={
        'orders':orders,
        
    }
    return render(request,'customer/my_orders.html',context)
def order_details(request,order_number):
    logger = logging.getLogger(__name__)
    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_food=OrderedFood.objects.filter(order=order)
        subtotal=0
        for item in ordered_food:
            subtotal+=(item.price*item.quantity)
        tax_data=json.loads(order.tax_data)
        context={
                'order':order,
                'ordered_food':ordered_food,
                'subtotal':subtotal,
                'tax_data':tax_data,
        }
        return render(request,'customer/order_details.html',context)
    except ObjectDoesNotExist:
        logger.warning(f"Order not found for user {request.user} with order_no {order_number}")
        
        return redirect('customer')