from fandb.models import Session,  Student
import sendgrid
import os
from sendgrid.helpers.mail import *

def send_mail():

    print '1'
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('DIJJJ'))
    p=os.environ.get('USER')
    print p
    print sg
    print os.environ.get('DIJJJ')
    print '2'
    from_email = Email("shubhamnagal296@gmail.co.in")
    subject = "Sending with SendGrid is Fun"
    to_email = Email("shubhamnagal296@gmail.co.in")
    print '3'
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    print '4'
    mail = Mail(from_email, subject, to_email, content)
    print '5'
    response = sg.client.mail.send.post(request_body=mail.get())
    print '6'
    print(response.status_code)
    print(response.body),'op'
    print(response.headers)




