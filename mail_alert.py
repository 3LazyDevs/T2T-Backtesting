# import smtplib
from email.message import EmailMessage
import smtplib
import ssl
import mcx
import futures as fut
data_mcx = mcx.get_comm_list()
data_fut = fut.get_all_symbols_list()
mx = False
fu = False
# list of email_id to send the mail
sender = "lazydev3@gmail.com"
receiver = "admin@trade2transform.com"
password = "vftt qjyt gyvo owcu"
if(data_mcx):
    mx = True
if(data_fut):
    fu = True

print("mx = ", mx, "fu = ", fu)

if(mx and fu):
    subject = "MCX and NSE are Live!"
    body = "Do check out the tool now as MCX API and NSE API are live now and data can be accessed!"

elif(mx):
    subject = "MCX is Live but NSE is down"
    body = "Check out the tool sometime later as NSE API is down, We will notify you once it is up!\n You can still use the tool to access MCX data"

elif(fu):
    subject = "NSE is Live but MCX is down"
    body = "Check out the tool sometime later as MCX API is down, We will notify you once it is up!\n You can still use the tool to access NSE data"

elif(fu):
    subject = "NSE and MCX are down"
    body = "Check out the tool sometime later as MCX API and NSE API are down, We will notify you once it is up!"

em = EmailMessage()
em['From'] = sender
em['To'] = receiver
em['Subject'] = subject
em.set_content(body)
context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, em.as_string())