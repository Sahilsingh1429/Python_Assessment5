from django.urls import path
from.views import *

urlpatterns = [
    path('',index,name='index'),
    path('register/',register,name='register'),
    path('register_submit/', register_submit, name='register_submit'),
    path('login/',login,name='login'),
    path('otp/',otp,name='otp'),
    path('total_user/',total_user,name='total_user'),
    path('buy_now/<int:pk>', buy_now, name='buy_now'),
    path('buy_now/paymenthandler/', paymenthandler, name='paymenthandler'),
    

]



#------------------COPIED CODE------------------------------#        
#         currency = 'INR'
#         global amount
#         amount = 1000 * 100 

#         # Create a Razorpay Order
#         razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                         currency=currency,
#                                                         payment_capture='0'))
    
#         # order id of newly created order.
#         razorpay_order_id = razorpay_order['id']
#         callback_url = 'paymenthandler/'
    
#         # we need to pass these details to frontend.
#         context = {}
#         context['razorpay_order_id'] = razorpay_order_id
#         context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#         context['razorpay_amount'] = amount
#         context['currency'] = currency
#         context['callback_url'] = callback_url
    
#         return render(request, 'buy_now.html', context=context)
       
#     except:
#         return redirect('login')
    

# """def test(request):
#     with open(os.path.join(settings.BASE_DIR, 'rzp.csv'), 'r') as f1:
#         list_of_lines = f1.readlines()
#         str1 = list_of_lines[-1]
#         final_list = str1.split(",")
#         razor_id = final_list[0]
#         razor_secret =  final_list[-1][:-1]
#         print(razor_secret)
#     return HttpResponse('ok')"""