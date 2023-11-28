"""
URL configuration for GreenForest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from . import views


urlpatterns = [
    path('', views.layout, name='home'),
    path('about/', views.about, name="about"),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('me/', views.me, name='me'),
    path('logout/', views.doLogout, name='logout'),
    path('cart/', views.view_cart, name='view_cart'),
    path('product_search/', views.product_search, name='product_search'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

]

