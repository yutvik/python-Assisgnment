from django.urls import path
from app_buyer import views
urlpatterns = [
    path('', views.index , name='index'),
    path('register/', views.register , name='register'),
    path('otp/', views.otp , name='otp'),
    path('login/', views.login , name='login'),
    path('logout/', views.logout , name='logout'),
    path('profile/', views.profile , name='profile'),
    path('update_profile/', views.update_profile , name='update_profile'),
    path('shop_product/', views.shop_product , name='shop_product'),
    path('show_details/<int:yk>', views.show_details , name='show_details'),
    path('add_to_cart/<int:yk>', views.add_to_cart , name='add_to_cart'),
    path('show_cart/', views.show_cart , name='show_cart'),
    path('remove_cart/<int:yk>', views.remove_cart , name='remove_cart'),
    path('update_cart/', views.update_cart , name='update_cart'),
    path('check_out/', views.check_out , name='check_out'),
    path('search/', views.search , name='search'),
    path('checkout/', views.checkout , name='checkout'),
    path('ram/', views.ram ),
    
 
    
    
    
    
    
    
    
    
    




    
]