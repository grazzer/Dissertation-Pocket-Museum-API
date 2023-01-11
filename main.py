from ast import arg
from logging import log
from flask import Flask
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String



app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user_artefact.db"
db = SQLAlchemy(app)


user_artefact = db.Table('user_artefact',
    db.Column('userId', db.Integer, db.ForeignKey('users.id')),
    db.Column('artefactId', db.Integer, db.ForeignKey('artifacts.id'))
)

class userModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25), nullable = False)
    collection = db.relationship("artefactModel", secondary=user_artefact, backref="collectors")

class artefactModel(db.Model):
    __tablename__ = 'artifacts'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25), nullable = False)
    discription = db.Column(db.String(250), nullable = False)
    Cultures = db.Column(db.String(25), nullable = False)
    productionPlace = db.Column(db.String(25), nullable = False)
    productionDate = db.Column(db.Integer, nullable = False)
    findCountry = db.Column(db.String(25), nullable = False)


# db.create_all()


Artefacts_resource_feilds = {
    "id": fields.Integer,
    "name": fields.String, 
    "discription": fields.String,
    "Cultures": fields.String,
    "productionPlace":fields.String,
    "productionDate":fields.String,
    "findCountry":fields.String
}

User_resource_feilds = {
    "id": fields.Integer,
    "name": fields.String
}

addArtefact = reqparse.RequestParser()
addArtefact.add_argument("id", type=int)
addArtefact.add_argument("name", type=String)
addArtefact.add_argument("discription", type=String)
addArtefact.add_argument("Cultures", type=String)
addArtefact.add_argument("productionPlace", type=String)
addArtefact.add_argument("productionDate", type=String)
addArtefact.add_argument("findCountry", type=String)

class Artefact(Resource):
    @marshal_with(Artefacts_resource_feilds)
    def get(self, artid):
        result = artefactModel.query.get(artid)
        return result

class user(Resource):
    @marshal_with(User_resource_feilds)
    def get(self, userid):
        result = userModel.query.get(userid)
        return result
    
    def patch(self, userid):
        args = addArtefact.parse_args()

        userResult = userModel.query.get(userid)
        artefactResult = artefactModel.query.get(args["id"])
        if not userResult:
            abort(404, message = "This user was not found")
        if not artefactResult:
            abort(404, message = "This artefact was not found")
        
        userResult.collection.append(artefactResult)
        db.session.commit()

        return 204
    
class Testing(Resource):
    def get(self, userid, artid):
        result = userModel.query.get(userid)
        art = artefactModel.query.get(artid)
        result.collection.remove(art)
        db.session.add(result)
        db.session.commit() 
        return "deleted"

class collection(Resource):
    @marshal_with(Artefacts_resource_feilds)
    def get(self, userid):
        user = userModel.query.get(userid)
        result = user.collection
        return result


api.add_resource(Artefact , "/artefact/<int:artid>")
api.add_resource(user , "/user/<int:userid>")
api.add_resource(collection , "/collection/<int:userid>")
api.add_resource(Testing , "/testing/<int:userid>/<int:artid>")
    
if __name__ == "__main__":
    app.run(debug=False)


# https://1133-138-37-230-124.eu.ngrok.io/testing/1/2
