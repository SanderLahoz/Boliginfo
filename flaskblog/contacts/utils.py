from flaskblog import mail
from flask_mail import Message
import os

def send_mail(name, email, subject, content):

	msg = Message(subject, 
		sender="noreply@contact-boliginfo.com",
		recipients=[os.environ.get("MAIL_USERNAME")])
	msg.body = f'''A user has submitted an invoice via the contact form
Name of sender: {name}
Email of sender: {email}

content: {content}

	'''

	mail.send(msg)
