from flask import jsonify
import secrets
from flask_security.utils import hash_password
from werkzeug.security import generate_password_hash
from flask_restful import Resource ,reqparse

from application.data.model import db,user

user_post_args= reqparse.RequestParser()
user_post_args.add_argument('user_mail',type=str,required=True)
user_post_args.add_argument('user_name',type=str,required=True)
user_post_args.add_argument('password',type=str,required=True)


class RegisterAPI(Resource):
	def post(self):
		args = user_post_args.parse_args()
		user_mail = args.get('user_mail')
		user_name = args.get('user_name')
		password = args.get('password')
		User = user.query.filter_by(user_mail=user_mail).first()
		if User :
			return jsonify({'status':'failed','message':'mail is already registered'})
			
		hashed_password = generate_password_hash(password)
		fs_uniquifier = secrets.token_hex(16)
		new_user = user(user_mail=user_mail,user_name=user_name,password=hashed_password,fs_uniquifier = fs_uniquifier,admin=False)
		# new_user.fs_uniquifier = secrets.token_hex(16)
		db.session.add(new_user)
		db.session.commit()
		
		return jsonify({'status':'Success','message':'Successfully Registered'})
	