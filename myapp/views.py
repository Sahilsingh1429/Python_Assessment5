from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.core.mail import send_mail
import random 
from django.conf import settings
from .models import *
import os
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Create your views here.
 
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 
def index(request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')


def register_submit(request):
    if request.POST['password'] == request.POST['re_password']:
        global g_otp, user_data
        user_data = [request.POST['f_name'], 
                     request.POST['l_name'],
                     request.POST['username'],
                     request.POST['email'],
                     request.POST['password']]
        g_otp = random.randint(100000, 999999)
        send_mail('Welcome Welcome',
                  f"Your OTP is {g_otp}",
                  settings.EMAIL_HOST_USER,
                  [request.POST['email']])
        return render(request, 'otp.html')        
    else:
        return render(request, 'register.html', {'msg': 'Both passwords do not MATCH'})

def login(request):
    if request.method =='GET':
        return render(request, 'login.html')
    else:
        try:
            d2 = User.objects.get(email = request.POST['email'])
            if request.POST['password'] == d2.password:
                request.session['user_email'] = request.POST['email']
                global user_obj
                user_obj = User.objects.get(email = request.session['user_email'])
                return render(request, 'index.html', {'userdata':d2})
            else:
                return render(request,'login.html', {'msg': 'Invalid Password'})
        except:
            return render(request, 'login.html', {'msg': 'email is not registered !!'})
def otp(request):
    try:
        if int(request.POST['u_otp']) == g_otp:
            User.objects.create(
                first_name = user_data[0],
                    last_name = user_data[1],
                    username = user_data[2],
                    email = user_data[3],
                    
                    password = user_data[4])
            return render(request, 'register.html', {'msg':'Successfully Registered!!'})
        else:
            return render(request, 'otp.html', {'msg': 'Invalid OTP, Enter again!!!'})
    except:
        return render(request, 'register.html')
    
def total_user(request):
        Show_user= Insurance.objects.all()
        return render(request,'total_user.html',{'tables':Show_user})
    
def add_user(request,pk):
    if request.method == 'GET':
        try:
            return render(request,'add_blog.html')
        
        except:
            return redirect('login')

def buy_now(request, pk):
    try:
         user_obj = User.objects.get(email = request.session['user_email'])
         global Ins_obj
         Ins_obj = Insurance.objects.get(id = pk)
    
    
    
    #------------------COPIED CODE------------------------------#        
         currency = 'INR'
         global amount
         amount = 1000 * 100 

        # Create a Razorpay Order
         razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
    
        # order id of newly created order.
         razorpay_order_id = razorpay_order['id']
         callback_url = 'paymenthandler/'
    
        # we need to pass these details to frontend.
         context = {}
         context['razorpay_order_id'] = razorpay_order_id
         context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
         context['razorpay_amount'] = amount
         context['currency'] = currency
         context['callback_url'] = callback_url
    
         return render(request, 'buy_now.html', context=context)
       
    except:
        return redirect('login')
    

"""def test(request):
    with open(os.path.join(settings.BASE_DIR, 'rzp.csv'), 'r') as f1:
        list_of_lines = f1.readlines()
        str1 = list_of_lines[-1]
        final_list = str1.split(",")
        razor_id = final_list[0]
        razor_secret =  final_list[-1][:-1]
        print(razor_secret)
    return HttpResponse('ok')"""
       
       
       
# ------------------------------------cpy-----------------------------------------




@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        user_obj = User.objects.get(email = request.session['user_email'])
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
                
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    Purchases.objects.create(
                        user_i = user_obj,
                        insurance_i = Ins_obj, 
                    )
                    return render(request, 'success.html')

                except:
 
                    # if there is an error while capturing payment.
                    return HttpResponse('paisa not found')
            else:
 
                # if signature verification fails.
                return HttpResponse('paisa not found')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
    
    
