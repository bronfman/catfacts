import json

from facts.models import PhoneNumber, CatFact 
from facts.forms import FactForm

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpRequest, HttpResponseRedirect

from twilio.rest import TwilioRestClient
from twilio.util import RequestValidator
from twilio.twiml import Response

from django_twilio.decorators import twilio_view


client = TwilioRestClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

def index(request):
    if request.method == 'POST':
        form = FactForm(request.POST)
        if form.is_valid():
            fact = form.cleaned_data['fact']
            catfact = CatFact()
            catfact.fact = fact
            catfact.save()
            
            messages.success(request, 'Catfact submited for approval!')
            return redirect('/')
        else:
            messages.error(request, 'Catfact was too long! It must be 120 characters or less')
            return redirect('/')
    else:
        form = FactForm()

    return render(request, 'index.html', {'form': form,})

def send_sms(to=None, from_=None, body=None):
    message = client.sms.messages.create(to=to, from_=from_, body=body)
    return message

def add_number(request):
    message = request.REQUEST.get('Body', None).lower()
    number = int(request.REQUEST['From'])
    from_ = request.REQUEST['To']

    catfact = CatFact.objects.filter(approved=True).order_by('?')[0]
    text = catfact.fact
    
    if message == "catfact":
        phone, created = PhoneNumber.objects.get_or_create(phonenumber=number)
        if created:
            message = send_sms(to=number, from_=from_, body="Thanks for signing up! Hope you enjoy CATFACTS!")
        else:
            message = send_sms(to=number, from_=from_, body="Cat Fact #" + str(catfact.id) + ": " + text)
            
        
    elif message == "nocats":
        phone, created = PhoneNumber.objects.get_or_create(phonenumber=number)
        phone.delete()
        message = send_sms(to=number, from_=from_, body="Sorry you had to go :( We'll miss you :(")

    elif message.split(' ')[0] == "add":
        num = message.split(' ')[1]
        phone, created = PhoneNumber.objects.get_or_create(phonenumber=num)
        if created:
            message = send_sms(to=number, from_=from_, body="Thanks for signing this person up! Hope they enjoy CATFACTS!")
            message2 = send_sms(to=num, from_=from_, body="Welcome to CATFACTS! You will now recieve a CATFACT every day! http://facts.cattes.us/")
        else:
            pass

    else:
        pass

    return HttpResponse("dongs")

def tell_fact(request):
    catfact = CatFact.objects.filter(approved=True).order_by('?')[0]
    return render(request, 'phonecall.html', {"fact": catfact}, content_type='application/xml')
