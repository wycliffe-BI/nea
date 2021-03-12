import os
from twilio.rest import Client

phone = "+447481339505"
rec = "+447597561844"

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages.create(
         body='This is the ship that made the Kessel Run in fourteen parsecs?',
         from_=phone,
         to=rec
     )

print(message.sid)
