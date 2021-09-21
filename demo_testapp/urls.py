from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('allCategories', views.allCategories, name='allCategories'),
    path('register', views.register, name='register'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('categories/logout', views.logout, name='logout'),
    path('categories/', views.categories, name='categories'),
    path('categories/categories', views.categories, name='categories'),
    path('contactUs', views.contactUs, name='contactUs'),
    path('new_search', views.new_search, name='new_search'),

    path('productForm/<int:id>/',views.productForm, name='productForm'),
    path('addToCart/<int:id>/', views.addToCart, name='addToCart'),
    path('moveToCart/<int:id>/', views.moveToCart, name='moveToCart'),
    path('removeFromCart/<int:id>/', views.removeFromCart, name='removeFromCart'),
    path('addToWishlist/<int:id>/', views.addToWishlist, name='addToWishlist'),
    path('moveToWishlist/<int:id>/', views.moveToWishlist, name='moveToWishlist'),
    path('removeFromWishlist/<int:id>/', views.removeFromWishlist, name='removeFromWishlist'),

    url('addToCart/<int:id>/home',views.home, name='home'),
    url('addToCart/<int:id>/categories',views.categories, name='categories'),
    url('addToCart/<int:id>/cart',views.cart, name='cart'),
    url('addToCart/<int:id>/logout',views.logout, name='logout'),
    url('cart',views.cart, name='cart'),

    url('addToWishlist/<int:id>/home',views.home, name='home'),
    url('addToWishlist/<int:id>/categories',views.categories, name='categories'),
    url('addToWishlist/<int:id>/wishlist',views.wishlist, name='wishlist'),
    url('addToWishlist/<int:id>/logout',views.logout, name='logout'),
    url('wishlist',views.wishlist, name='wishlist'),

    url('payment',views.payment, name='payment'),


]
