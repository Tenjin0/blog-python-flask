from app import app, mail
from flask_mail import Message
msg = Message('test subject', sender=app.config['ADMINS'][0],
              recipients=['petitpatrice@gmail.com'])
msg.body = 'text body'
msg.html = '<h1>HTML body</h1>'
with app.app_context():
    mail.send(msg)
