from django.shortcuts import render
from.models import *
from django.conf import settings
from django.core.mail import send_mail
from seller_buyer.models  import *
from django.db.models import Q
import requests
from django.contrib.auth.hashers import make_password,check_password
import random
# Create your views here.
def index(request):
    return render(request,"index.html")


def register(request):
    if request.method=="POST":
        api_key = 'sNqOjnjE.iqpUFUKYmgDLIwxMdtnupmEOzYogpez9' # Generated in your User Profile it shows at the top in a green bar once
        team_slug = "yutvik" # when you sign up you have a team, its in the URL then use that
        email_address =request.POST["email"]# the test email


        response = requests.post(
            "https://app.mailvalidation.io/a/" + team_slug + "/validate/api/validate/",
            json={'email': email_address},
            headers={
                    'content-type': 'application/json',
                    'accept': 'application/json',
                    'Authorization': 'Api-Key ' + api_key,
                    },
        )

        valid = response.json()['is_valid']
        if valid:
            if request.POST["cpassword"]== request.POST["password"]:
            
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
                return render(request,"otp.html")
            
            else:
                return render(request,"register.html",{"msg":"Email not Valid"})    
        else:
            return render(request,"register.html",{"msg":"Password And Confirm Password not mach"})
    else:
        return render(request,"register.html")  #get method
    
def otp(request):
    if request.method=="POST":
        if user_otp==int(request.POST["OTP"]):
            User.objects.create(
                firstname=temp["firstname"],
                lastname=temp["lastname"],
                email=temp["email"],
                password=make_password(temp["password"]),
            )
            return render(request,"register.html",{"msg":"registaions successfull"})
        else:
                return render(request,"otp.html",{"msg":"OTP NOT MACHED"})



def login(request):
    if request.method=="POST":
        try:
            user_data=User.objects.get(email=request.POST["email"])
            if check_password(request.POST["password"],user_data.password):
                 request.session["email"]=request.POST["email"]
                 return render(request,"four-col.html",{"user_data":user_data})
                 
            else:
              return render(request,"login.html",{"msg":"password Not Match"})
        except:
            return render(request,"login.html",{"msg":"we cannot find an account with that email address"})
    else:
            return render(request,"login.html")   
    
def logout(request):
    del request.session["email"]
    return render(request,"login.html",{"msg":"Logout Sucessfull"})
    

def profile(request):
    user_data=User.objects.get(email=request.session["email"])
    return render(request,"profile.html",{"user_data":user_data})
    

def update_profile(request):
    if request.method=="POST":
        user_data=User.objects.get(email=request.session["email"])
        try:
            pro_image=request.FILES["propic"]
        except:
            pro_image=user_data.picture
        if request.POST["npassword"]:
            if check_password(request.POST["opassword"],user_data.password):
                if request.POST["cpassword"]==request.POST["npassword"]:
                    user_data.firstname=request.POST["fname"]
                    user_data.lastname=request.POST["lname"]
                    user_data.password=make_password(request.POST["npassword"])
                    user_data.picture=pro_image
                    user_data.save()
                else:
                    return render(request,"profile.html",{"user_data":user_data,"msg":"New Password and Confirm Passwod Not Match"})
            else:
                return render(request,"profile.html",{"user_data":user_data,"msg":"Old Password Not Match"})
        else:
            user_data.firstname=request.POST["fname"]
            user_data.lastname=request.POST["lname"]
            user_data.picture=pro_image
            user_data.save()
            return render(request,"profile.html",{"user_data":user_data,"msg":"Profile Updated Successfully"})
    else:
            user_data=User.objects.get(email=request.session["email"])
            return render(request,"profile.html",{"user_data":user_data})
        
        
def shop_product(request):
    user_data=User.objects.get(email=request.session["email"])
    all_product=Product.objects.all()
    return render(request,"products.html",{"all_product":all_product,'user_data':user_data})    



def show_details(request,yk):
    user_data=User.objects.get(email=request.session["email"])
    one_product=Product.objects.get(id=yk)
    return render(request,"product_details.html",{"one_product":one_product,'user_data':user_data})
        

        
def add_to_cart(request,yk):
    
    user_data=User.objects.get(email=request.session["email"])  
    try:
        product=Product.objects.get(id=yk)
        exists_user_data=Cart.objects.get( Q(pro_id=yk)  &  Q(buyer_id=user_data.id)) 
        exists_user_data.qut+=1 
        exists_user_data.total=exists_user_data.qut*exists_user_data.pro_id.p_price
        exists_user_data.save()
        return show_cart(request)  
        
    except:
        product=Product.objects.get(id=yk)
        Cart.objects.create(
            pro_id=product,
            buyer_id=user_data,
            qut=1,
            total=product.p_price
        )
    return show_cart(request) 


def show_cart(request):
    user_data=User.objects.get(email=request.session["email"])
    all_cart=Cart.objects.filter(buyer_id=user_data.id)
    
    final_total=0
    for i in all_cart:
        final_total=final_total+i.total
    return render(request,"cart.html",{"all_cart":all_cart,"final_total":final_total,"user_data":user_data})



def remove_cart(request,yk):
    one_cart=Cart.objects.get(id=yk)
    one_cart.delete()
    return show_cart(request) 


def update_cart(request):
    user_data=User.objects.get(email=request.session["email"]) 
    if request.method=="POST":
        l1=request.POST.getlist("quantity")
        all_cart=Cart.objects.filter(buyer_id=user_data.id)
        for i,j in zip(all_cart,l1):
            i.qut=j
            i.total=int(j)*i.pro_id.p_price
            i.save()
            
        return show_cart(request)
    else:
        return show_cart(request)
             
def check_out(request):
    user_data=User.objects.get(email=request.session["email"])
    all_cart=Cart.objects.filter(buyer_id=user_data.id)
    final_total=0
    for i in all_cart:
        final_total=final_total+i.total
    return render(request,'check_out.html',{"all_cart":all_cart,"final_total":final_total,"user_data":user_data})     


def search(request):
    user_data=User.objects.get(email=request.session["email"])
    if request.method=="POST":
        search=request.POST["search_Q"]
        data=Product.objects.filter(Q(p_name__icontains=search) | Q(p_dec__icontains=search))
        return render(request,"products.html",{"user_data":user_data,"data":data})
 
 
def checkout(request):
    user_data=User.objects.get(email=request.session["email"])
    all_cart=Cart.objects.filter(buyer_id=user_data.id)
    if request.method=="POST":
        Checkout.objects.create(
           FirstName=request.POST["fname"],
           MiddleName=request.POST["mname"], 
           LastName=request.POST["lname"],
           Address=request.POST["Address"],
           postelcode=request.POST["postel"],
           State=request.POST["state"],
           PhoneNumber=request.POST["Phone"],
        )
        final_total=0
        for i in all_cart:
            final_total=final_total+i.total
        return render(request,"paymeat.html",{"user_data":user_data,"all_cart":all_cart,"final_total":final_total})
    else:
        return render(request,"check_out.html",{"user_data":user_data})    
    
        
        
        
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

	# only accept POST request.
	if request.method == "POST":
		try:
		
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is not None:
				amount = 20000 # Rs. 200
				try:

					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)

					# render success page on successful caputre of payment
					return render(request, 'paymentsuccess.html')
				except:

					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()



from rest_framework.decorators import api_view
from rest_framework.response import Response
from app_buyer.serializers import Checkout_serializers
from app_buyer.models import Checkout


@api_view(['GET'])
def ram(request):
        all_data=Checkout.objects.all()
        serial =Checkout_serializers(all_data,many=True)
        return Response(serial.data)

                
        
        
        
        
        
       

       
        
            

        
   
    