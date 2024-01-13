from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('category_api/', views.category_list, name='category_list'),
    path('product_api/', views.product_list, name='product_list'),
    path('users_api/', views.user_list, name='user_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('viewcart/', views.viewcart, name='viewcart'),
    path('addtocart/<int:id>/', views.addtocart, name='addtocart'),
    path('removefromcart/<int:id>/', views.removefromcart, name='removefromcart'),
    path('increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('myorders/', views.myorders, name='myorders'),
    path('shop/', views.shop, name='shop'),
    path('shop/<str:category>/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('thankyou/', views.thankyou, name='thankyou'),
    path('product_detail/<str:name>/',views.product_detail, name='product_detail'),

    ]
