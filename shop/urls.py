from django.urls import path, re_path
from . import views

urlpatterns = [
    path('logout/', views.logout_user, name='signout'),
    path('', views.index, name='index'),
    re_path(r'^shop/(?P<q>\w*)/$', views.shop, name='shop'),
    path('search/', views.search, name='search'),
    path('product/<int:id>/', views.view_product, name='view-product'),
    path('filter/', views.filter, name='filter'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('order/<int:id>/delete', views.delete_order, name='delete-order'),

    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),

    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    
]
