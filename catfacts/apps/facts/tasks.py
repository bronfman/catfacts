from django.conf import settings

from twilio.rest import TwilioRestClient

from celery.task.schedules import crontab
from celery.decorators import periodic_task, task
from datetime import timedelta

from facts.models import PhoneNumber, CatFact


client = TwilioRestClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

def send_sms(to=None, from_=None, body=None):
    message = client.sms.messages.create(to=to, from_=from_, body=body)
    return message

@task()
def poop_facts(number, from_,  message):
    send_sms(to=number, from_=from_, body=message)

@periodic_task(run_every=timedelta(hours=24))
def send_fact():
    numbers = PhoneNumber.objects.all()
    fact = CatFact.objects.filter(approved=True).order_by('?')[0]

    text = "CATFACT #%s: %s" % (fact.id, fact.fact)

    for n in numbers:
        poop_facts.delay(n, settings.PHONE_NUMBER, text)

    




