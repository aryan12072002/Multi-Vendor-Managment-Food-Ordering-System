from django.urls import path
from accounts import views as AccountView
from . import views
urlpatterns = [
    path('',AccountView.customerDashboard,name='customer'),
    path('profile/',views.cprofile,name='cprofile'),
    path('my_orders/',views.my_orders,name='customer_my_orders'),
    path('order_details/<int:order_number>/',views.order_details,name='order_details'),
    
    
]
