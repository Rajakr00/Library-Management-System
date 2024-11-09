import json
from flask import request,jsonify
from flask_restful import Resource,reqparse,abort,fields, marshal_with
from flask_jwt_extended.view_decorators import jwt_required
from datetime import datetime

from sqlalchemy import Integer


# importing model from database
from application.data.model import db,Section,Ebook,book_issue, user

book_issue_post_args= reqparse.RequestParser()
book_issue_post_args.add_argument('user_id',type=int,required=True)
book_issue_post_args.add_argument('ebook_id',type=int,required=True)


class IssueRequestAPi(Resource):
    @jwt_required()
    def post(self):
        args=book_issue_post_args.parse_args()
        user_id=args['user_id']
        ebook_id = args['ebook_id']

        issue_book_re = book_issue.query.filter_by(user_id=user_id , ebook_id=ebook_id).first()

        if issue_book_re :
            issue_book_re.status='pending'
            db.session.commit()
            return ({ "status" :"Requested Sent Successfully",})
            
        issue_request = book_issue(user_id=user_id,ebook_id=ebook_id,status='pending',issue_date=None,return_date=None)
        db.session.add(issue_request)
        db.session.commit()
        return ({ "status" :"Requested Sent Successfully",})
    
class fetch_IssuerequestAPI(Resource):
    @jwt_required()
    def get(self):
        requested_book = book_issue.query.filter_by().all()
        req_pending = []
        for pending_request in requested_book:
            if (pending_request.status != 'available'):
                User = user.query.get(pending_request.user_id)
                book = Ebook.query.get(pending_request.ebook_id)
                req_pending.append({"id":pending_request.id,"user_id":pending_request.user_id,"user_name": User.user_name if user else None,"book_id":pending_request.ebook_id,"book_name": book.name if book else None,"status":pending_request.status})
        return req_pending
    
class checkIssuerequestAPI(Resource):
    @jwt_required()
    def get(self,user_id):
        check_issue = book_issue.query.filter_by(user_id=user_id).all()
        req_pending = []
        if check_issue:
            for issue_req in check_issue:
                if (issue_req.return_date) :
                    req_pending.append({issue_req.ebook_id:(issue_req.status,  issue_req.return_date)})
                else :
                    req_pending.append({issue_req.ebook_id:issue_req.status})
            return req_pending
        return ({"status":"available"})

book_grant_post_args= reqparse.RequestParser()
book_grant_post_args.add_argument('return_date',type=str,required=True)
class GrantIssueAPI(Resource):
    @jwt_required()
    def post(self,id):
        args=book_grant_post_args.parse_args()
        return_date = args['return_date']

        grant_request=book_issue.query.filter_by(id=id).first()

        if not grant_request:
            return ({"message":"error"})
        
        grant_request.return_date=return_date
        grant_request.issue_date = datetime.now()
        grant_request.status="Success"
        db.session.commit()
        return jsonify({"message":"successfully granted","return":return_date,"grant":id})

class RevokeGrantAPI(Resource):
    @jwt_required()
    def put(self,id):

        revoke_request=book_issue.query.filter_by(id=id).first()

        if not revoke_request:
            return ({"message":"error"})
        
        revoke_request.return_date = None
        revoke_request.issue_date = None
        revoke_request.status="available"
        db.session.commit()
        return jsonify({"message":"successfully revoked"})
    
    
