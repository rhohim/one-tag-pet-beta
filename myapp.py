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
database = 'sqlite:///' + os.path.join(filename, 'condfe.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['SECRET_KEY'] = "cretivoxtechnology22"

class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(100))
    stock = db.Column(db.Integer)
    receipt = db.Column(db.Integer)
    
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

class Colorpost(Resource):
    def post(self):
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        if auth_header == "Bearer aldikaburgataukemanabawassdtiktokkatanyaprivasi":
            datacolor = request.form.get('color')
            datastock = request.form.get('stock')
            datareceipt = request.form.get('receipt')
            dataModel = Color(color=datacolor, stock= datastock, receipt= datareceipt)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg":"success"}), 200)
        else:
            return jsonify({"msg":"Failed"})
    
    def get(self):
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        if auth_header == "Bearer aldikaburgataukemanabawassdtiktokkatanyaprivasi":
            print("sama")
            dataQuery = Color.query.all()
            output = []
            for i in range(len(dataQuery)):
                val = {
                    "id" : dataQuery[i].id,
                    "data" : {
                        "color" : dataQuery[i].color,
                        "stock" : dataQuery[i].stock,
                        "receipt" : dataQuery[i].receipt
                    }
                }
                output.append(val)

            return make_response(jsonify(output), 200)
        else:
            return jsonify({"msg":"Failed"}) 
    
    def delete(self):
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        if auth_header == "Bearer aldikaburgataukemanabawassdtiktokkatanyaprivasi":
            db.session.query(Color).delete()
            db.session.commit()
                
            return jsonify({"msg":"Deleted"}) 
        else:
            return jsonify({"msg":"Failed"})
        
class Colorid(Resource):
    def get(self, id):
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        if auth_header == "Bearer aldikaburgataukemanabawassdtiktokkatanyaprivasi":
            print("sama")
            data = Color.query.filter(Color.id == id).first()
            output = []
    
            val = {
                "id" : data.id,
                "data" : {
                    "color" : data.color,
                    "stock" : data.stock,
                    "receipt" : data.receipt
                }
            }
            output.append(val)

            return make_response(jsonify(output), 200)
        else:
            return jsonify({"msg":"Failed"})
        
    def put(self,id):
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        if auth_header == "Bearer aldikaburgataukemanabawassdtiktokkatanyaprivasi":
            print("sama")
            dataUpdate = Color.query.filter(Color.id == id).first()
            # datacolor = request.form.get('color')
            # datastock = request.form.get('stock')
            datastock = dataUpdate.stock
            totalreceipt = dataUpdate.receipt
            datareceipt = 1
            
            datastock = int(datastock) - datareceipt
            
            # dataUpdate.color = datacolor
            dataUpdate.stock = datastock
            dataUpdate.receipt = int(totalreceipt) + datareceipt
            db.session.commit()
            return make_response(jsonify({"msg" : "updated"}), 200)
        else:
            return jsonify({"msg":"Failed"})
    
    def delete(self,id):
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        if auth_header == "Bearer aldikaburgataukemanabawassdtiktokkatanyaprivasi":
            print("sama")
            own = Color.query.filter(Color.id == id).first()
            db.session.delete(own)
            db.session.commit()
            return make_response(jsonify({"msg" : "deleted"}), 200)
        else:
            return jsonify({"msg":"Failed"})
        
class Coloredit(Resource):
    def put(self,id):
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        if auth_header == "Bearer aldikaburgataukemanabawassdtiktokkatanyaprivasi":
            print("sama")
            dataUpdate = Color.query.filter(Color.id == id).first()
            # datacolor = request.form.get('color')
            datastock = request.form.get('stock')
            print(datastock)
            # dataUpdate.color = datacolor
            dataUpdate.stock = datastock
            dataUpdate.receipt = 0
            db.session.commit()
            return make_response(jsonify({"msg" : "updated"}), 200)
        else:
            return jsonify({"msg":"Failed"})

api.add_resource(Colorpost, "/condfe/color", methods=["GET", "POST", "DELETE"])
api.add_resource(Colorid, "/condfe/color/<id>", methods=["PUT", "GET", "DELETE"])
api.add_resource(Coloredit, "/condfe/color/stock/<id>", methods=["PUT"])            
            
if __name__ == "__main__":
    app.run(debug=True,port=2012, host="0.0.0.0")            
        
        