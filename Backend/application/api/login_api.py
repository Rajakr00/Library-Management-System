from flask import jsonify
from flask_restful import Resource,reqparse
from flask_security import login_user
from flask_security.utils import verify_password,hash_password
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity
from werkzeug.security import check_password_hash
from application.data.model import db,user 


parser = reqparse.RequestParser()
parser.add_argument('user_mail',type=str,required=True)
parser.add_argument('password',type=str,required=True)



# api for login

class LoginAPI(Resource):
	def post(self):
		args = parser.parse_args()
		user_mail = args.get('user_mail')
		password = args.get('password')


		filter_user = user.query.filter_by(user_mail=user_mail).first()

		# if user not exit throw error

		if filter_user is None :
			return jsonify({'status':'failed','message':'user doesnt exist'})

		#  check for user password
		plain_password = password
		hashed_password = filter_user.password

		if not check_password_hash(hashed_password,plain_password):
			return jsonify({ 'status':'Failed','message':'wrong password'})
			
		
		
		refresh_token = create_refresh_token(identity=filter_user.user_id)
		access_token = create_access_token(identity=filter_user.user_id)

		login_user(filter_user)
		return jsonify({'status':'Success','message':'Successfully logged In',"refresh_token":refresh_token,"access_token":access_token,"user_mail":filter_user.user_mail,"admin":filter_user.admin,"user_id":filter_user.user_id})


class RefreshTokenAPI(Resource):
	@jwt_required(refresh=True)
	def post(self):
		identity = get_jwt_identity()
		access_token = create_access_token(identity=identity)
		return {'access_token': access_token},200