from flask import Flask, request, make_response, jsonify, Response
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy 
from functools import wraps


import jwt 
import os 
import datetime 
from cryptography.fernet import Fernet

#send email
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)
api = Api(app)

CORS(app)
UPLOAD_FOLDER = '/home/u1739959/rest-api/cv'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

application = app



filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'dbemail.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = "cretivoxtechnology22"
key = b'qXkOeccBROMqPi3MCFrNc6czJDrEJopBOpoWWYBKdpE='
fernet = Fernet(key)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    wanumber = db.Column(db.Text)
    desc = db.Column(db.Text)
    
db.create_all()

class UpMsg(Resource):
    def post(self):
        datasub = request.form.get('subject')
        databod = request.form.get('body')
        smtp_port = 587                 
        smtp_server = "smtp.gmail.com"  
        email_from = "getpc2022@gmail.com"
        pswd = "twbpnvymsfthaqfr"
        

        person = "qna@onasis-indonesia.co.id"
        # Make the body of the email
        # body = f'''
        # {''.join(databod)}
        # '''
        body = databod

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person
        msg['Subject'] = datasub


        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))

        
        text = msg.as_string()

        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Succesfully connected to server")
        print()


        print(f"Sending email to: {person}...")
        TIE_server.sendmail(email_from, person, text)
        print(f"Email sent to: {person}")
        print()

        TIE_server.quit()
        
        return jsonify({"msg":"Success"})
    
api.add_resource(UpMsg, "/api/contact", methods=["POST"])


if __name__ == "__main__":
    app.run(debug=True,port=2023, host="0.0.0.0")