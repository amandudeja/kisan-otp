from django.shortcuts import (render,get_object_or_404,redirect)
from contacts.models import Contact,Sent
from django.utils.crypto import get_random_string
from twilio.rest import Client
from django.conf import settings
import datetime
from django.contrib import messages


# Create your views here.
def homepage(request):
	contacts = Contact.objects.all()
	return render(request,'base.html',{'contacts':contacts})


def detail(request,contact_id):
	contact = get_object_or_404(Contact,pk=contact_id)
	print(str(contact.mobile)+'\n'+contact.first_name)
	return render(request,'contacts/details.html',{'contact':contact})

def sendform(request,contact_id):
	contact = get_object_or_404(Contact,pk=contact_id)
	otp = get_random_string(length=6,allowed_chars='123456789')
	# temp = otp

	if request.method=="POST":
		if request.POST['body']:
			to = "+91"+str(contact.mobile)
			body = request.POST['body']
			otp = request.POST['otp']
			print("SEDNING TO:"+to)
			print("TEXT:-"+body)
			
			try:
				client = Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
				response = client.messages.create(body=body,to=to,from_=settings.TWILIO_PHONE_NUMBER)
				newmsg = Sent.objects.create(mobile=contact,sent_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),otp=otp)
				print(otp)
				messages.add_message(request, messages.SUCCESS,
				'Message Sent Successfully at {}.'.format(str(contact.mobile)))
				# print(newmsg)
			except:
				messages.add_message(request, messages.ERROR,
				'Message cannot be sent as {} is not verified with your Twilio Account!.'.format(str(contact.mobile)))
			return redirect('home')

	else:
		return render(request,'contacts/sendform.html',{'otp':otp,'contact':contact})

def sentmessages(request):
	sents = Sent.objects.order_by('-sent_time')
	# print(sents)
	return render(request,'contacts/sent.html',{'sents':sents})


def adduser(request):
	if request.method=="POST":
		if request.POST['firstname'] and request.POST['lastname'] and request.POST['mobile']:
			newuser = Contact.objects.create(first_name=request.POST['firstname'],
				last_name=request.POST['lastname'],mobile=request.POST['mobile'])
			return redirect('home')

	return render(request,'contacts/new_user.html',{})



