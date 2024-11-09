from flask import Flask
from flask_restful import Api,Resource
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from celery.schedules import crontab
from application.cache import cache

import redis


from application.security import security, user_datastore


import application.config as config
from application.data.database import db
from application.data.model import user

app = Flask(__name__)
app.config.from_object(config)
app.app_context().push()

# redis_client = redis.Redis(host='localhost',port=6379,db=0)
# cache = Cache(app,config={'CACHE_TYPE':'redis','CACHE_REDIS':redis_client})

CORS(app,origins='*')

db.init_app(app)

api = Api(app)

security.init_app(app, user_datastore)

api.init_app(app)

JWTManager(app)

cache.init_app(app)

# importing api 
from application.api.register_api import RegisterAPI
from application.api.login_api import LoginAPI
from application.api.login_api import RefreshTokenAPI

from application.api.section_api import AllSectionAPI
from application.api.section_api import sectionAPI
from application.api.section_api import sectionEditAPI
from application.api.ebook_api import AllEbooksapi
from application.api.ebook_api import EbookAPI
from application.api.section_api import CreateSectionAPI
from application.api.ebook_api import Ebook_remove_Api
from application.api.book_issue import IssueRequestAPi
from application.api.book_issue import fetch_IssuerequestAPI
from application.api.book_issue import GrantIssueAPI
from application.api.book_issue import RevokeGrantAPI
from application.api.book_issue import checkIssuerequestAPI



api.add_resource(RegisterAPI,"/api/register")
api.add_resource(LoginAPI,"/api/login")
api.add_resource(RefreshTokenAPI, "/api/token/refresh")


api.add_resource(CreateSectionAPI, "/api/section/create")
api.add_resource(AllSectionAPI, "/api/section/home")
api.add_resource(sectionAPI, "/api/section/<int:section_id>")
api.add_resource(sectionEditAPI, "/api/section/edit/<int:section_id>")
api.add_resource(AllEbooksapi,"/api/section/home/<int:section_id>")
api.add_resource(EbookAPI,"/api/section/home/book")
api.add_resource(Ebook_remove_Api,"/api/section/home/book/<int:ebook_id>")
api.add_resource(IssueRequestAPi,"/api/request_book")
api.add_resource(fetch_IssuerequestAPI,"/api/request_book/fetch")
api.add_resource(GrantIssueAPI,"/api/request_book/fetch/<int:id>")
api.add_resource(checkIssuerequestAPI,"/api/request/<int:user_id>")
api.add_resource(RevokeGrantAPI,"/api/request_book/revoke/<int:id>")




with app.app_context():
	db.create_all()

@app.route("/")
def home():
	return "<html> <h1> Hello Raja </h1></html>"

if __name__ == '__main__':
	app.run(host="0.0.0.0",port=5000,debug=True)