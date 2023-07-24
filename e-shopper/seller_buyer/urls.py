from django.urls import path
from seller_buyer import views
urlpatterns = [
    path('', views.seller_index , name='seller_index'),
    path('seller_register/', views.seller_register , name='seller_register'),
    path('seller_otp/', views.seller_otp , name='seller_otp'),
    path('seller_login/', views.seller_login , name='seller_login'),
    path('seller_logout/', views.seller_logout , name='seller_logout'),
    path('seller_profile/', views.seller_profile , name='seller_profile'),
    path('seller_update_profile/', views.seller_update_profile , name='seller_update_profile'),
    path('add_product/', views.add_product , name='add_product'),
    path('live_product/', views.live_product , name='live_product'),
    path('listing_update/<int:y>', views.listing_update , name='listing_update'),
    path('delete/<int:y>', views.delete , name='delete'),
    path('seller_order/', views.seller_order , name='seller_order'),
    
    
    
    
    
    
    

]