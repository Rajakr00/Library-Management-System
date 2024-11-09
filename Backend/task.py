import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import csv
from io import StringIO
from datetime import datetime
from celery_config import celery
from application.data.model import db,user,book_issue,Ebook
from celery.schedules import crontab
from main import app
@celery.task
def MONTHLY_REPORT():
    with app.app_context():
        current_month = datetime.now().strftime('%B')
        current_year = datetime.now().year
        users = user.query.filter_by(admin=False).all()

    for User in users:
        book=book_issue.query.filter_by(user_id=User.user_id).all()
        count=len(book)
        book_name =[]
        for books in book :
            ebook = Ebook.query.filter_by(ebook_id=books.ebook_id).first()
            book_name.append(ebook.name)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <title> Monthly Summary </title>
        </head>
        <body>
        <h1> Monthly Report -{ current_month} {current_year}</h1>
        <p> Hello {User.user_name}</p>
        <p> Here is your summary of the book issued of the month {current_month}</p>
        <ul>
        <li> Total book issued:{count}
        <ul> Books Name:</ul>
        <ul>{book_name}
        </ul>
        
        <p> Thanku for using the Online library</p>
        <p> Keep Learning</p>
        </body>
        </html>
        """
        send_email(User.user_mail,html_content)

def send_email(to_email,html_content):
    from_email = 'rajakumar85418211289@gmail.com'
    subject = 'Monthly Report'

    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    part = MIMEText(html_content,'html')
    msg.attach(part)

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'rajakumar8541821289@gmail.com'
    smtp_password = 'zvbb sqnm aydz qkmz'

    with smtplib.SMTP(smtp_server,smtp_port) as server:
        server.starttls()
        server.login(smtp_username,smtp_password)
        server.sendmail(from_email,to_email,msg.as_string())
