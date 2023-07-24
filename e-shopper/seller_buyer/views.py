from django.shortcuts import render
from.models import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password,check_password
from app_buyer.models import *
# Create your views here.
def seller_index(request):
    return render(request,"seller_index.html")


def seller_register(request):
    if request.method=="POST":
         if request.POST["cpassword"]== request.POST["password"]:
            import random
            global user_otp
            user_otp=random.randint(100000,999999)    
            subject = 'OTP VERIFICATIONS PROCESS JEWEL WORLD'
            message = f'thank for chooisng us your otp is {user_otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST ["email"], ]
            send_mail( subject, message, email_from, recipient_list)
            global temp
            temp={
                "firstname":request.POST["fname"],
                "lastname":request.POST["lname"],
                "email":request.POST["email"],
                "password":request.POST["password"],



            }
            return render(request,"seller_otp.html")
         else:
             return render(request,"seller_register.html",{"msg":"Password And Confirm Password not mach"})
    else:
         return render(request,"seller_register.html")  #get method
def seller_otp(request):
    if request.method=="POST":
        if user_otp==int(request.POST["otp"]):
            seller_User.objects.create(
                firstname=temp["firstname"],
                lastname=temp["lastname"],
                email=temp["email"],
                password=make_password(temp["password"]),
            )
            return render(request,"seller_register.html",{"msg":"registaions successfull"})
        else:
              return render(request,"seller_otp.html",{"msg":"OTP NOT MACHED"})
        
def seller_login(request):
    if request.method=="POST":
        try:
            user_data=seller_User.objects.get(email=request.POST["email"])
            if check_password(request.POST["password"],user_data.password):
                 request.session["seller_email"]=request.POST["email"]
                 return render(request,"seller_four-col.html",{"user_data":user_data})
                 
            else:
              return render(request,"seller_login.html",{"msg":"password Not Match"})
        except:
            return render(request,"seller_login.html",{"msg":"we cannot find an account with that email address"})
    else:
            return render(request,"seller_login.html") 
      
def seller_logout(request):
    user_data=seller_User.objects.get(email=request.session["seller_email"])
    del request.session["seller_email"]
    return render(request,"seller_login.html",{"msg":"LogOut Suceesfull","user_data":user_data}) 

def seller_profile(request):
    user_data=seller_User.objects.get(email=request.session["seller_email"])
    return render(request,"seller_profile.html",{"user_data":user_data})  


def seller_update_profile(request):
    if request.method=="POST":
        user_data=seller_User.objects.get(email=request.session["seller_email"])
        if request.POST["npassword"]:
            try:
                picture_image=request.FILES["propic"]  #image na aave to use thai/error aave aetle try use karelu
            except:
                picture_image=user_data.picture  #image aave to use thai 
            if check_password(request.POST["opassword"],user_data.password):
                if request.POST["cpassword"]==request.POST["npassword"]:
                    user_data.firstname=request.POST["fname"]
                    user_data.lastname=request.POST["lname"]
                    user_data.password=make_password(request.POST["npassword"])
                    user_data.picture=picture_image
                    user_data.save()
                else:
                    return render(request,"seller_profile.html",{"user_data":user_data,"msg":"New Password and Confirm Passwod Not Match"})
            else:
                return render(request,"seller_profile.html",{"user_data":user_data,"msg":"Old Password Not Match"})
        else:
            user_data.firstname=request.POST["fname"]
            user_data.lastname=request.POST["lname"]
            user_data.picture=picture_image
            user_data.save()
        return render(request,"seller_index.html",{"user_data":user_data,"msg":"Profile Updated Successfully"})
    else:
            user_data=seller_User.objects.get(email=request.session["seller_email"])
            return render(request,"seller_profile.html",{"user_data":user_data})

def add_product(request):
    seller_user=seller_User.objects.get(email=request.session["email"])
    if request.method=="POST":
        Product.objects.create(
            p_name=request.POST["p_name"],
            p_price=request.POST["p_price"],
            p_image=request.FILES["p_image"],
            p_qut=request.POST["p_qut"],
            p_dec=request.POST["p_dec"],
            seller_id=seller_user
        )
        return render(request,"add_product.html",{"msg":"Product Added Successfully"})
    else:
         return render(request,"add_product.html")
     
     

def view_product(request):
        seller_user=seller_user.objects.get(email=request.session["email"])
        my_product=Product.objects.filter(id=seller_user)
        return render(request,"my_product.html",{"my_product":my_product} ) 
    
         

def live_product(request):
    seller_user=seller_User.objects.get(email=request.session["email"])
    all_data=Product.objects.filter(seller_id=seller_user)
    return render(request,"live_product.html",{"all_data":all_data})
   
def listing_update(request,y):
    seller_user=seller_User.objects.get(email=request.session["email"])
    if request.method=="POST":
        one_data=Product.objects.get(id=y)
        one_data.p_name=request.POST["p_name"]
        one_data.p_image=request.FILES["p_image"]
        one_data.p_qut=request.POST["p_qut"]
        one_data.p_price=request.POST["p_price"]
        one_data.p_dec=request.POST["p_dec"]
        one_data.save()
        all_data=seller_User.object.all()
        return render(request,"listing_update.html",{"all_data,":all_data})
    else:
        one_data=Product.objects.get(id=y)
        return render(request,"listing_update.html",{"one_data":one_data}) 
    
       
def delete(request,y):      
    seller_user=seller_User.objects.get(email=request.session["email"])  
    one_data=Product.objects.get(id=y)
    one_data.delete()
    all_data=seller_User.objects.all()
    one_data.save()
    return render(request,"live_product.html",{"seller_user":seller_user,"one_data":one_data,"all_data":all_data})

def seller_order(request):
    seller_user=seller_User.objects.get(email=request.session["email"])  
    all_order=Cart.objects.filter(pro_id__seller_id=seller_user)
    return render(request,"seller_order.html",{"seller_user":seller_user,"all_order":all_order})   

 