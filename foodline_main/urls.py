"""
URL configuration for foodline_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import home
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views as marketplaceview
from marketplace import views as cartview
urlpatterns = [
    path("admin/", admin.site.urls),
    path("",home,name='home'),
    path("accounts/",include("accounts.urls")),
    path("marketplace/",include("marketplace.urls")),
    path("search/",marketplaceview.search,name='search'),
        #view cart
    path('cart/',cartview.cart,name='cart'),
    #chaeckout
    path("checkout/",marketplaceview.checkout,name='checkout'),
    path('orders/',include('orders.urls')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
