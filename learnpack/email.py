from django.core.mail import EmailMultiAlternatives
from rest_framework.exceptions import APIException
import os
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
import requests


def send_email_message(slug, to, data={}):
    print('Email notification '+slug+' sent')
    if settings.EMAIL_NOTIFICATIONS_ENABLED:
        template = get_template_content(slug, data, ["email"])
        print('ENABLED')
        return requests.post(
            f"https://api.mailgun.net/v3/{os.environ.get('MAILGUN_DOMAIN')}/messages",
            auth=(
                "api",
                os.environ.get('MAILGUN_API_KEY')),
            data={
                "from": f" <mailgun@{os.environ.get('MAILGUN_DOMAIN')}>",
                "to": to,
                "subject": template['subject'],
                "text": template['text'],
                "html": template['html']}).status_code == 200
    else:
        print('Email not sent because notifications are not enabled')
        return True


def get_template_content(slug, data={}, formats=None):
    info = data

    #d = Context({ 'username': username })
    con = {
        'API_URL': os.environ.get('API_URL'),
        'COMPANY_NAME': 'LearnPack',
        'COMPANY_LEGAL_NAME': 'LearnPack LLC',
        'COMPANY_ADDRESS': '270 Catalonia, Coral Gables, 33134'
    }
    z = con.copy()   # start with x's keys and values
    z.update(data)

    templates = {
        "subject": info['subject']
    }

    if formats is None or "email" in formats:
        plaintext = get_template(slug + '.txt')
        html = get_template(slug + '.html')
        templates["text"] = plaintext.render(z)
        templates["html"] = html.render(z)

    if formats is not None and "fms" in formats:
        fms = get_template(info['type'] + '/' + slug + '.fms')
        templates["fms"] = fms.render(z)

    if formats is not None and "sms" in formats:
        sms = get_template(info['type'] + '/' + slug + '.sms')
        templates["sms"] = sms.render(z)

    return templates


