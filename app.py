# import library flask 
from flask import Flask, request, make_response, jsonify, Response
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy 
from functools import wraps
from cryptography.fernet import Fernet


import jwt 
import os 
import datetime 
from datetime import date

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
CORS(app)

#setting database
filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['SECRET_KEY'] = "cretivoxtechnology22"


#make database and column
class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
    ig = db.Column(db.String(100))
    email = db.Column(db.String(50))
    location = db.Column(db.Text)
    img = db.Column(db.Text)
    name = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    pets = db.relationship('TagPet', backref="owner")


class TagPet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String(50)) 
    pet_picture_img = db.Column(db.Text)
    pet_picture_name = db.Column(db.Text)
    pet_picture_mimetype = db.Column(db.Text)
    pet_age =  db.Column(db.String(50))
    pet_ras = db.Column(db.String(50))
    pet_gender = db.Column(db.String(50))
    pet_vaccine =  db.Column(db.String(50))
    pet_story = db.Column(db.String(50)) 
    pet_type = db.Column(db.String(255)) 
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))

class Ads(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    dsc = db.Column(db.Text)
    img = db.Column(db.Text)
    name = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    datadate = db.Column(db.Text)

# db.drop_all()
db.create_all()

key = b'qXkOeccBROMqPi3MCFrNc6czJDrEJopBOpoWWYBKdpE='
fernet = Fernet(key)


def token_api(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = ""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        
        # token = request.args.get('token') 
        if not token:
            return make_response(jsonify({"msg":"there is no token"}), 401)
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return make_response(jsonify({"msg":"invalid token"}), 401)
        return f(*args, **kwargs)
    return decorator


class RegisterUser(Resource):
    def post(self):
        
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')
        # dataig = request.form.get('ig')
        dataEmail = request.form.get('email')
        # dataloc = request.form.get('location')
        
        #get image
        # pic = request.files['image']
        
        # print(dataig, dataloc, pic)
        
        # if not pic :
        #     return jsonify({"msg" : "picture not allowed"})
        # filename = secure_filename(pic.filename)
        # mimetype = pic.mimetype
        # if not filename or not mimetype:
        #     return jsonify({"msg":"bad upload"})
        

        if dataUsername and dataPassword:
            print("in")
            # dataModel = Owner(username=dataUsername, password=dataPassword, email=dataEmail, ig = dataig, location= dataloc,
            #                   img=pic.read(), name = filename , mimetype =mimetype)
            dataModel = Owner(username=dataUsername, password=dataPassword, email=dataEmail)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg":"success"}), 200)
        return jsonify({"msg":"Username / password is empty"})
    
class Profile(Resource):
    @token_api
    def get(self):
        token = ""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        # print(decoded_token['superadmin'])
        data = Owner.query.filter(Owner.id == id).first()
        if decoded_token["username"] == "admin":
            dataQuery = Owner.query.all()
            output = []
            for i in range(len(dataQuery)):
                # print(dataQuery[i].name)
                # if dataQuery[i].name == None :
                #     url = ""
                if dataQuery[i].name:
                    # print("in")
                    url = "192.168.1.253:1234/owner/picture/" + str(dataQuery[i].id)
                else:
                    # print("out")
                    url = None
                val = {
                "id" : dataQuery[i].id,
                "data" : 
                    {
                        "name" : dataQuery[i].username,
                        "email" : dataQuery[i].email,
                        "instagram" : dataQuery[i].ig,
                        "location" : dataQuery[i].location,
                        "profile" : url
                    }
                }
                output.append(val)

            return make_response(jsonify(output), 200)
    
    @token_api
    def delete(self):
        token = ""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        # print(decoded_token['superadmin'])
        data = Owner.query.filter(Owner.id == id).first()
        if decoded_token["username"] == "admin":
            db.session.query(Owner).delete()
            db.session.commit()
            
            return jsonify({"msg":"Deleted"})    
    
    
class GetImgOwner(Resource):
    def get(self, id):
        print(id)
        img = Owner.query.filter(Owner.id == id).first()
        # print(img.img)
        if not img:
           return jsonify({"msg":"bad request"}) 
        return Response(img.img, mimetype=img.mimetype) 
    


class Account(Resource):
    @token_api
    def get(self, id):
        # admin = "admin"
        token = ""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        # print(decoded_token['superadmin'])
        data = Owner.query.filter(Owner.id == id).first()
        #encrypt & dcrypt password
        # x = fernet.encrypt(data.password.encode())
        # print(data.password)
        # print(fernet.encrypt(data.password.encode()))
        # print(fernet.decrypt(bytes(x).decode()))
        
        if decoded_token["username"] == "admin":
            data = Owner.query.filter(Owner.id == id).first()
            # print(data.name) 
            if data.name:
                # print("in")
                url = "192.168.1.253:1234/owner/picture/" + str(data.id)
            else:
                # print("out")
                url = None
            output = [{
                "id" : data.id,
                "data" : 
                    {
                        "name" : data.username,
                        "email" : data.email,
                        "instagram" : data.ig,
                        "location" : data.location,
                        "profile" : url
                    }
                
            } 
            ]

            return make_response(jsonify(output), 200)
        if (data.username != decoded_token["username"]):
            return jsonify({"msg":"Access Denied"})
        else:
            data = Owner.query.filter(Owner.id == id).first()
            # print(data.name) 
            if data.name:
                # print("in")
                url = "192.168.1.253:1234/owner/picture/" + str(data.id)
            else:
                # print("out")
                url = None
            output = [{
                "id" : data.id,
                "data" : 
                    {
                        "name" : data.username,
                        "email" : data.email,
                        "instagram" : data.ig,
                        "location" : data.location,
                        "profile" : url
                    }
                
            } 
            ]

            return make_response(jsonify(output), 200)
    
    @token_api
    def put(self,id):
        token = ""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        data = Owner.query.filter(Owner.id == id).first()
        if decoded_token["username"] == "admin":
            dataUpdate = Owner.query.filter(Owner.id == id).first()
            dataUsername = request.form.get('username')
            # dataPassword = request.form.get('password')
            dataig = request.form.get('ig')
            dataEmail = request.form.get('email')
            dataloc = request.form.get('location')
            
            #get image
            pic = request.files['image']
            print("PIC " , pic)
            if not pic :
                return jsonify({"msg" : "picture not allowed"})
            filename = secure_filename(pic.filename)
            mimetype = pic.mimetype
            if not filename or not mimetype:
                return jsonify({"msg":"bad upload"})
            
            dataUpdate.username = dataUsername
            # dataUpdate.dataPassword = dataPassword
            dataUpdate.ig = dataig
            dataUpdate.email = dataEmail
            dataUpdate.location = dataloc
            dataUpdate.img = pic.read()
            dataUpdate.name = filename
            dataUpdate.mimetype = mimetype
            
            db.session.commit()
            
            return make_response(jsonify({"msg" : "updated"}), 200)
        if data.username != decoded_token["username"]:
            return jsonify({"msg":"Access Denied"})
        else:
            dataUpdate = Owner.query.filter(Owner.id == id).first()
            dataUsername = request.form.get('username')
            # dataPassword = request.form.get('password')
            dataig = request.form.get('ig')
            dataEmail = request.form.get('email')
            dataloc = request.form.get('location')
            
            #get image
            pic = request.files['image']
            print(dataUsername, dataig, dataEmail, dataloc)
            print("PIC " , pic)
            if not pic :
                return jsonify({"msg" : "picture not allowed"})
            filename = secure_filename(pic.filename)
            mimetype = pic.mimetype
            if not filename or not mimetype:
                return jsonify({"msg":"bad upload"})
            
            dataUpdate.username = dataUsername
            # dataUpdate.dataPassword = dataPassword
            dataUpdate.ig = dataig
            dataUpdate.email = dataEmail
            dataUpdate.location = dataloc
            dataUpdate.img = pic.read()
            dataUpdate.name = filename
            dataUpdate.mimetype = mimetype
            
            db.session.commit()
            
            return make_response(jsonify({"msg" : "updated"}), 200)
    
    @token_api
    def delete(self, id):
        print(id)
        token = ""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        data = Owner.query.filter(Owner.id == id).first()
        if decoded_token["username"] == "admin":
            own = Owner.query.filter(Owner.id == id).first()
            db.session.delete(own)
            db.session.commit()
            return make_response(jsonify({"msg" : "deleted"}), 200)
        if data.username != decoded_token["username"]:
            return jsonify({"msg":"Access Denied"})
        else:
            own = Owner.query.filter(Owner.id == id).first()
            db.session.delete(own)
            db.session.commit()
            return make_response(jsonify({"msg" : "deleted"}), 200)


class LoginUser(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        dbOwner= Owner.query.all()
        
        queryUsername = [data.username for data in Owner.query.all()]
        queryPassword = [data.password for data in Owner.query.all()]
        if dataUsername in queryUsername and dataPassword in queryPassword :
            token = jwt.encode(
                {
                    "username":dataUsername, "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
                }, app.config['SECRET_KEY'],  algorithm="HS256"
            )
            for i in range(len(dbOwner)):
                if dbOwner[i].username == dataUsername:
                    id = dbOwner[i].id
            return make_response(jsonify({"msg":"Welcome", "token":token, "id":id}), 200)
        return jsonify({"msg":"failed"})
    
    

class AddTag(Resource):
    @token_api
    def post(self):
        
        dataPetname = request.form.get('pet_name') 
        dataPetage = request.form.get('pet_age') 
        dataPetgender = request.form.get('pet_gender') 
        dataPetvaccine = request.form.get('pet_vaccine')
        dataPetras = request.form.get('pet_ras') 
        dataStory = request.form.get('pet_story') 
        datatype = request.form.get('pet_type') 
        dataOwner = request.form.get('owner')
        
        pic = request.files['image']

        if not pic :
            return jsonify({"msg" : "picture not allowed"})
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return jsonify({"msg":"bad upload"})
        
        # dbOwner= Owner.query.all()
        
        # queryowner = [data.username for data in Owner.query.all()]
        # if dataOwner in queryowner:
        #     for i in range(len(dbOwner)):
        #         if dbOwner[i].username == dataOwner:
        #             id = dbOwner[i].id
        # else:
        #     return {"msg":"there is no owner name"}        
            
        # print(id)
        data = TagPet(pet_name = dataPetname, pet_ras = dataPetras, pet_age = dataPetage ,pet_gender = dataPetgender,
                      pet_vaccine =  dataPetvaccine,pet_picture_img = pic.read(), pet_picture_name = filename, pet_type = datatype,
                      pet_picture_mimetype = mimetype,pet_story = dataStory, owner_id= dataOwner)
        db.session.add(data)
        db.session.commit()
        return{"msg":"success"}, 200

    # @token_api
    def get(self):
        dataQuery = TagPet.query.all()
        output = []
        print(dataQuery[0].owner.ig)
        for i in range(len(dataQuery)):
            val = {
                "id" : dataQuery[i].id,
                "data" : {
                    "pet_name": dataQuery[i].pet_name,
                    "pet_age": dataQuery[i].pet_age,
                    "pet_gender": dataQuery[i].pet_gender,
                    # "pet_vaccine": dataQuery[i].pet_vaccine,
                    "pet_ras": dataQuery[i].pet_ras,
                    "pet_story": dataQuery[i].pet_story,
                    "pet_type" : dataQuery[i].pet_type,
                    "pet_image": "192.168.1.253:1234/pet/picture/" + str(dataQuery[i].id),
                    "owner" : dataQuery[i].owner.username,
                    "ig" : dataQuery[i].owner.ig
                }
            }
            output.append(val)

        return make_response(jsonify(output), 200)
    
    @token_api
    def delete(self):
        token = ""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        # print(decoded_token['superadmin'])
        data = Owner.query.filter(Owner.id == id).first()
        if decoded_token["username"] == "admin":
            db.session.query(TagPet).delete()
            db.session.commit()
            
            return jsonify({"msg":"Deleted"}) 
    
class GetImgPet(Resource):
    def get(self, id):
        print(id)
        img = TagPet.query.filter(TagPet.id == id).first()
        # print(img.img)
        if not img:
           return jsonify({"msg":"bad request"}) 
        return Response(img.pet_picture_img, mimetype=img.pet_picture_mimetype) 
    
class AddTagTo(Resource):
    def get(self, id):
        data = TagPet.query.filter(TagPet.id == id).first()
        output = [{
           "id" : data.id,
            "data" : {
                "pet_name": data.pet_name,
                "pet_age": data.pet_age,
                "pet_gender": data.pet_gender,
                "pet_vaccine": data.pet_vaccine,
                "pet_ras": data.pet_ras,
                "pet_story": data.pet_story,
                "pet_type" : data.pet_type,
                "pet_image": "192.168.1.251:1234/pet/picture/" + str(data.id)
            }
            
        } 
        ]

        return make_response(jsonify(output), 200)
    
    @token_api
    def put(self,id):
        token = ""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        datapet = TagPet.query.filter_by(id = id).all()
        print(datapet[0].owner.username)
        # data = Owner.query.filter(Owner.id == id).first()
        if decoded_token["username"] == "admin":
            dataUpdate = TagPet.query.filter(TagPet.id == id).first()
            dataPetname = request.form.get('pet_name') 
            dataPetage = request.form.get('pet_age') 
            dataPetgender = request.form.get('pet_gender') 
            dataPetvaccine = request.form.get('pet_vaccine')
            dataPetras = request.form.get('pet_ras') 
            dataStory = request.form.get('pet_story') 
            datatype = request.form.get('pet_type') 
            dataOwner = request.form.get('owner')
            
            pic = request.files['image']
            
            # if dataPetvaccine == "True":
            #     dataPetvaccine = True
            # elif dataPetvaccine == "False":
            #     dataPetvaccine = False
            if not pic :
                return jsonify({"msg" : "picture not allowed"})
            filename = secure_filename(pic.filename)
            mimetype = pic.mimetype
            if not filename or not mimetype:
                return jsonify({"msg":"bad upload"})
            
            # dbOwner= Owner.query.all()
            
            # queryowner = [data.username for data in Owner.query.all()]
            # if dataOwner in queryowner:
            #     for i in range(len(dbOwner)):
            #         if dbOwner[i].username == dataOwner:
            #             id = dbOwner[i].id
            # else:
            #     return {"msg":"there is no owner name"}
            # print(dataPetvaccine)
            dataUpdate.pet_name = dataPetname
            dataUpdate.pet_picture_img = pic.read()
            dataUpdate.pet_picture_name = filename
            dataUpdate.pet_picture_mimetype = mimetype
            dataUpdate.pet_age = dataPetage
            dataUpdate.pet_ras = dataPetras
            dataUpdate.pet_gender = dataPetgender
            dataUpdate.pet_vaccine = dataPetvaccine
            dataUpdate.pet_story = dataStory
            dataUpdate.pet_type = datatype
            dataUpdate.owner_id = dataOwner
            
            db.session.commit()
            
            return make_response(jsonify({"msg" : "updated"}), 200)
        if datapet[0].owner.username != decoded_token["username"]:
            return jsonify({"msg":"Access Denied"})
        else:
            dataUpdate = TagPet.query.filter(TagPet.id == id).first()
            dataPetname = request.form.get('pet_name') 
            dataPetage = request.form.get('pet_age') 
            dataPetgender = request.form.get('pet_gender') 
            dataPetvaccine = request.form.get('pet_vaccine')
            dataPetras = request.form.get('pet_ras') 
            dataStory = request.form.get('pet_story') 
            datatype = request.form.get('pet_type') 
            dataOwner = request.form.get('owner')
            
            pic = request.files['image']
            
            # if dataPetvaccine == "True":
            #     dataPetvaccine = True
            # elif dataPetvaccine == "False":
            #     dataPetvaccine = False
            if not pic :
                return jsonify({"msg" : "picture not allowed"})
            filename = secure_filename(pic.filename)
            mimetype = pic.mimetype
            if not filename or not mimetype:
                return jsonify({"msg":"bad upload"})
            
            # dbOwner= Owner.query.all()
            
            # queryowner = [data.username for data in Owner.query.all()]
            # if dataOwner in queryowner:
            #     for i in range(len(dbOwner)):
            #         if dbOwner[i].username == dataOwner:
            #             id = dbOwner[i].id
            # else:
            #     return {"msg":"there is no owner name"}
            # print(dataPetvaccine)
            dataUpdate.pet_name = dataPetname
            dataUpdate.pet_picture_img = pic.read()
            dataUpdate.pet_picture_name = filename
            dataUpdate.pet_picture_mimetype = mimetype
            dataUpdate.pet_age = dataPetage
            dataUpdate.pet_ras = dataPetras
            dataUpdate.pet_gender = dataPetgender
            dataUpdate.pet_vaccine = dataPetvaccine
            dataUpdate.pet_story = dataStory
            dataUpdate.pet_type = datatype
            dataUpdate.owner_id = dataOwner
            
            db.session.commit()
            
            return make_response(jsonify({"msg" : "updated"}), 200)
    @token_api
    def delete(self, id):
        print(id)
        token = ""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        datapet = TagPet.query.filter_by(id = id).all()
        print(datapet[0].owner.username)
        # data = Owner.query.filter(Owner.id == id).first()
        if decoded_token["username"] == "admin":
            own = TagPet.query.filter(TagPet.id == id).first()
            db.session.delete(own)
            db.session.commit()

            return make_response(jsonify({"msg" : "deleted"}), 200) 
        if datapet[0].owner.username != decoded_token["username"]:
            return jsonify({"msg":"Access Denied"})
        else:
            own = TagPet.query.filter(TagPet.id == id).first()
            db.session.delete(own)
            db.session.commit()

            return make_response(jsonify({"msg" : "deleted"}), 200)

    
class TagOwn(Resource):
    def get(self):
        dataQuery = TagPet.query.all()
        # print(dataQuery[0].owner.username)
        dataPet, datatag = [], []
        lastid = 0
        for data in dataQuery:
            dataPet = []
            if lastid != data.owner_id:
                pet = TagPet.query.filter_by(owner_id = data.owner_id).all()
                print(pet)
                for i in range(len(pet)):
                    valuepet = {
                        "id" : pet[i].id,
                        "data" : {
                            "pet_name": pet[i].pet_name,
                            "pet_age": pet[i].pet_age,
                            "pet_gender": pet[i].pet_gender,
                            "pet_vaccine": pet[i].pet_vaccine,
                            "pet_ras": pet[i].pet_ras,
                            "pet_story": pet[i].pet_story,
                            "pet_type" : pet[i].pet_type,
                            "pet_image": "192.168.1.251:1234/pet/picture/" + str(pet[i].id)
                            }
                    }
                    
                    dataPet.append(valuepet)
                if pet[i].owner.name:
                    # print("in")
                    url = "192.168.1.253:1234/owner/picture/" + str(pet[i].owner.id)
                else:
                    # print("out")
                    url = None    
                valueown = {
                    "id" : pet[i].owner.id,
                    "name" : pet[i].owner.username,
                    "email" : pet[i].owner.email,
                    "instagram" : pet[i].owner.ig,
                    "location" : pet[i].owner.location,
                    "profile" : url
                }
                out = {
                    "pets" : dataPet,
                    "owner" : valueown
                }
                datatag.append(out)
            lastid = data.owner_id

        return make_response(jsonify(datatag), 200)
    
class TagOwnTo(Resource):
    @token_api
    def get(self,id):
        token = ""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        # print(decoded_token["username"])
        data = Owner.query.filter(Owner.id == id).first()
        # print(dataQuery[0].owner.username)
        dataPet, datatag = [], []
        dataPet = []
        if decoded_token["username"] == "admin":
            pet = TagPet.query.filter_by(owner_id = id).all()
            print(pet)
            if data.name:
                # print("in")
                url = "192.168.1.253:1234/owner/picture/" + str(data.id)
            else:
                # print("out")
                url = None 
            if len(pet) == 0 :
                valueown = {
                    "id" : data.id,
                    "name" : data.username,
                    "email" : data.email,
                    "instagram" : data.ig,
                    "location" : data.location,
                    "profile" : url
                }
                out = {
                    "pets" : dataPet,
                    "owner" : valueown
                }
                datatag.append(out)
                return make_response(jsonify(datatag), 200)
            else:
                for i in range(len(pet)):
                    valuepet = {
                        "id" : pet[i].id,
                        "data" : {
                            "pet_name": pet[i].pet_name,
                            "pet_age": pet[i].pet_age,
                            "pet_gender": pet[i].pet_gender,
                            "pet_vaccine": pet[i].pet_vaccine,
                            "pet_ras": pet[i].pet_ras,
                            "pet_story": pet[i].pet_story,
                            "pet_type" : pet[i].pet_type,
                            "pet_image": "192.168.1.253:1234/pet/picture/" + str(pet[i].id)
                            }
                    }
                    
                    dataPet.append(valuepet)
                if pet[0].owner.name:
                    # print("in")
                    url = "192.168.1.253:1234/owner/picture/" + str(pet[0].owner.id)
                else:
                    # print("out")
                    url = None        
                valueown = {
                    "id" : pet[i].owner.id,
                    "name" : pet[i].owner.username,
                    "email" : pet[i].owner.email,
                    "instagram" : pet[i].owner.ig,
                    "location" : pet[i].owner.location,
                    "profile" : url
                }
                out = {
                    "pets" : dataPet,
                    "owner" : valueown
                }
                datatag.append(out)
                    

                return make_response(jsonify(datatag), 200) 
        if data.username != decoded_token["username"]:
            return jsonify({"msg":"Access Denied"})
        else:
            # print("good")
            pet = TagPet.query.filter_by(owner_id = id).all()
            print(pet)
            if data.name:
                # print("in")
                url = "192.168.1.253:1234/owner/picture/" + str(data.id)
            else:
                # print("out")
                url = None 
            if len(pet) == 0 :
                valueown = {
                    "id" : data.id,
                    "name" : data.username,
                    "email" : data.email,
                    "instagram" : data.ig,
                    "location" : data.location,
                    "profile" : url
                }
                out = {
                    "pets" : dataPet,
                    "owner" : valueown
                }
                datatag.append(out)
                return make_response(jsonify(datatag), 200)
            else:
                for i in range(len(pet)):
                    valuepet = {
                        "id" : pet[i].id,
                        "data" : {
                            "pet_name": pet[i].pet_name,
                            "pet_age": pet[i].pet_age,
                            "pet_gender": pet[i].pet_gender,
                            "pet_vaccine": pet[i].pet_vaccine,
                            "pet_ras": pet[i].pet_ras,
                            "pet_story": pet[i].pet_story,
                            "pet_type" : pet[i].pet_type,
                            "pet_image": "192.168.1.253:1234/pet/picture/" + str(pet[i].id)
                            }
                    }
                    
                    dataPet.append(valuepet)
                if pet[0].owner.name:
                    # print("in")
                    url = "192.168.1.253:1234/owner/picture/" + str(pet[0].owner.id)
                else:
                    # print("out")
                    url = None        
                valueown = {
                    "id" : pet[i].owner.id,
                    "name" : pet[i].owner.username,
                    "email" : pet[i].owner.email,
                    "instagram" : pet[i].owner.ig,
                    "location" : pet[i].owner.location,
                    "profile" : url
                }
                out = {
                    "pets" : dataPet,
                    "owner" : valueown
                }
                datatag.append(out)
                    

                return make_response(jsonify(datatag), 200)

class AdsAs(Resource):
    @token_api
    def post(self):
        token = ""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        # data = Owner.query.filter(Owner.id == id).first()
        if decoded_token["username"] == "admin":
            d2 = date.today()
            datatitle = request.form.get('title') 
            datadsc = request.form.get('description')
            pic = request.files['image']

            if not pic :
                return jsonify({"msg" : "picture not allowed"})
            filename = secure_filename(pic.filename)
            mimetype = pic.mimetype
            if not filename or not mimetype:
                return jsonify({"msg":"bad upload"})
            
            data = Ads(datadate = d2 , title = datatitle, dsc = datadsc, img = pic.read(), mimetype = mimetype, name= filename)
            db.session.add(data)
            db.session.commit()
            return{"msg":"success"}, 200
        
    def get(self):
        dataQuery = Ads.query.all()
        output = []
        for i in range(len(dataQuery)):
            val = {
                "id" : dataQuery[i].id,
                "data" : {
                    "title" : dataQuery[i].title,
                    "description" : dataQuery[i].dsc,
                    "date" : dataQuery[i].datadate,
                    "image" : "192.168.1.253:1234/ads/picture/" + str(dataQuery[i].id),
                }
            }
            output.append(val)

        return make_response(jsonify(output), 200)
    @token_api
    def delete(self):
        token = ""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        datapet = TagPet.query.filter_by(id = id).all()
        print(datapet[0].owner.username)
        # data = Owner.query.filter(Owner.id == id).first()
        if decoded_token["username"] == "admin":
            db.session.query(Ads).delete()
            db.session.commit()
                
            return jsonify({"msg":"Deleted"})    

class GetAds(Resource):
    def get(self, id):
        print(id)
        img = Ads.query.filter(Ads.id == id).first()
        # print(img.img)
        if not img:
           return jsonify({"msg":"bad request"}) 
        return Response(img.img, mimetype=img.mimetype)

class AdsAsTo(Resource):
    def get(self, id):
        data = Ads.query.filter(Ads.id == id).first()
        output = [{
           "id" : data.id,
            "data" : {
                "title" : data.title,
                "description" : data.dsc,
                "date" : data.datadate,
                "image": "192.168.1.253:1234/ads/picture/" + str(data.id)
            }
            
        } 
        ]

        return make_response(jsonify(output), 200)   
    
    @token_api
    def put(self, id):
        token = ""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        datapet = TagPet.query.filter_by(id = id).all()
        print(datapet[0].owner.username)
        # data = Owner.query.filter(Owner.id == id).first()
        if decoded_token["username"] == "admin":
            dataUpdate = Ads.query.filter(Ads.id == id).first()
            datatitle = request.form.get('title') 
            datadsc = request.form.get('description') 
            
            
            pic = request.files['image']
            
            if not pic :
                return jsonify({"msg" : "picture not allowed"})
            filename = secure_filename(pic.filename)
            mimetype = pic.mimetype
            if not filename or not mimetype:
                return jsonify({"msg":"bad upload"})
            
            dataUpdate.title = datatitle
            dataUpdate.dsc = datadsc
            dataUpdate.img = pic.read()
            dataUpdate.name = filename
            dataUpdate.mimetype = mimetype
        
            
            db.session.commit()
            
            return make_response(jsonify({"msg" : "updated"}), 200)

    @token_api
    def delete(self, id):
        token = ""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        datapet = TagPet.query.filter_by(id = id).all()
        print(datapet[0].owner.username)
        # data = Owner.query.filter(Owner.id == id).first()
        if decoded_token["username"] == "admin":
            own = Ads.query.filter(Ads.id == id).first()
            db.session.delete(own)
            db.session.commit()

            return make_response(jsonify({"msg" : "deleted"}), 200)        
# inisiasi resource api 

#Register user & owner (POST)
api.add_resource(RegisterUser, "/api/register", methods=["POST"])

api.add_resource(Profile, "/api/profile", methods = ["GET" , "DELETE"])
api.add_resource(Account,"/api/profile/<id>", methods=["GET", "DELETE", "PUT"])

#login and get token (POST)
api.add_resource(LoginUser, "/api/login", methods=["POST"])

#Add pet data (POST), see pet data (GET), (DELETE) pet by name
api.add_resource(AddTag, "/api/tag", methods=["GET", "POST", "DELETE"])
api.add_resource(AddTagTo,"/api/tag/<id>", methods=["GET", "DELETE", "PUT"])

#(GET) all data pet and owner relation
api.add_resource(TagOwn, "/api/tag/all", methods=["GET"])
api.add_resource(TagOwnTo, "/api/tag/all/<id>", methods=["GET"])

api.add_resource(AdsAs, "/api/sa/ads", methods=["GET", "POST", "DELETE"])
api.add_resource(AdsAsTo, "/api/sa/ads/<id>", methods=["GET", "PUT", "DELETE"])

api.add_resource(GetImgOwner, "/owner/picture/<id>", methods=["GET"])
api.add_resource(GetImgPet, "/pet/picture/<id>", methods=["GET"])
api.add_resource(GetAds, "/ads/picture/<id>", methods=["GET"])

if __name__ == "__main__":
    app.run(debug=True,port=1234, host="0.0.0.0")




