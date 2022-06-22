from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View,CreateView,ListView
from django.contrib.auth.models import User
from app10.forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login,logout
from app10.forms import AddCategoryForm,AddSubscriptionForm
from app10.models import *

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Create your views here.
class homeview(TemplateView):
	template_name='home.html'

class featureview(TemplateView):
	template_name='feature.html'


class aboutusview(TemplateView):
	template_name='aboutus.html'

class RegisterView(View):
	template_name='register.html'

class workinghoursview(TemplateView):
	template_name='workinghours.html'

	def get(self,request):
		context={'form':UserRegisterForm}
		return render(request,self.template_name,context)

	def post(self,request):
		username=request.POST.get('username')
		password=request.POST.get('password1')
		email=request.POST.get('email')
		first_name=request.POST.get('first_name')
		last_name=request.POST.get('last_name')
		user=User.objects.create(username=username,
			password=password,
			email=email,
			first_name=first_name,
			last_name=last_name,
			is_staff=True)
		user.set_password(password)
		user.save()
		return redirect('register')

class UserLogin(View):
	def get(self,request):
		form=AuthenticationForm()
		context={'form':form}
		return render(request,'login.html',context)

	def post(self,request):
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(username=username,password=password)
		if user is not None :
			login(request,user)	
		if user.is_superuser==True and user.is_staff ==True:
			return redirect('home')
		if user.is_staff==True and user.is_superuser ==False:
			return redirect('home')
		if user.is_staff ==False and user.is_superuser ==False:
			return redirect('home')
		else:
			form=AuthenticationForm()	
			context={'form':form}
			return render(request,'login.html',context)

def logout_view(request):
	logout(request)	
	return redirect('home')

class AddCategoryView(CreateView):
	template_name='category.html'
	form_class=AddCategoryForm
	success_url='/'

class AddSubscriptionView(CreateView):
	template_name='subscription.html'
	form_class=AddSubscriptionForm
	success_url='/'

class CategorylistView(ListView):
	template_name='categorylist.html'
	model=AddCategoryModel
	context_object_name='data'

class SubscriptionListView(ListView):
	template_name='sublist.html'
	model=AddSubscriptionModel
	context_object_name='data'

class SubBookView(View):
	template_name='subbook.html'

	def get(self,request,pk):
		data=AddSubscriptionModel.objects.get(id=pk)
		user=request.user
		name=data.name 
		duration=data.duration
		feestructure=data.feestructure
		category=data.category

		SubBookModel.objects.create(user=user,
			name=name,
			duration=duration,
			feestructure=feestructure,
			Category=category)

		return redirect ('pay')
# 		

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

class PaymentView(View):
	template_name="payment.html"

	def get(self,request):
		data=SubBookModel.objects.last()
		amount=int(data.feestructure)*100
		currency = 'INR'
		# amount = 20000  # Rs. 200
 
		# Create a Razorpay Order
		razorpay_order = razorpay_client.order.create(dict(amount=amount,
		currency=currency,payment_capture='0'))
		print("order",razorpay_order)
 
		# order id of newly created order.
		razorpay_order_id = razorpay_order['id']
		callback_url = '/paymenthandler/'
 
		# we need to pass these details to frontend.
		context = {'amount_rupee':data.feestructure}
		context['razorpay_order_id'] = razorpay_order_id
		context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
		context['razorpay_amount'] = amount
		context['currency'] = currency
		context['callback_url'] = callback_url
		print(context)
 
		return render(request,self.template_name, context=context)
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

	print('Payment is started---------------------------------->')
 
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
			print(params_dict)
 
			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			print("RESULT-------------------------------> ", result)
			if result is not None:
				# amount = 20000  # Rs. 200
				data=SubBookModel.objects.last()
				amount=int(data.feestructure)*100
				print("---------------------------------> AMOUNT: ", amount, "TYPE: ", type(amount))
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
