import json
from flask import request,jsonify
from flask_restful import Resource,reqparse,abort,fields, marshal_with
from flask_jwt_extended.view_decorators import jwt_required
from application.cache import cache

from application.data.model import db,Section,Ebook
from application.data.All_data_access import get_all_ebook

# this is to add the ebook
ebooks_post_args =reqparse.RequestParser()
ebooks_post_args.add_argument('name',type=str,required=True)
ebooks_post_args.add_argument('content',type=str)
ebooks_post_args.add_argument('authors',type=str,required=True)
ebooks_post_args.add_argument('section_id',type=int,required=True)

# ebooks_post_args.add_argument('book_pdf',type=str,)

# put requist to ediot
ebooks_put_args=reqparse.RequestParser()
ebooks_put_args.add_argument('name',type=str,required=True)
ebooks_put_args.add_argument('content',type=str)
ebooks_put_args.add_argument('authors',type=str,required=True)


resource_field = {
    'ebook_id':fields.Integer,
    'name':fields.String,
    'content':fields.String,
    'authors':fields.String,
    'section_id':fields.Integer
    # 'book_pdf':fields.LargeBinary
}


class AllEbooksapi(Resource):
   @cache.cached(timeout=2)
   @jwt_required()

   def get(self,section_id):
        ebook_f = Ebook.query.all()

        # ebooks_f = get_all_ebook()
        sec_book = []
        for book in ebook_f:
            if book.section_id == section_id :
                sec_book.append({"ebook_id":book.ebook_id,"name":book.name,"content":book.content,"authors":book.authors})
        return sec_book
    
class EbookAPI(Resource):
    @jwt_required()
    @marshal_with(resource_field)

    def post(resource):
        args = ebooks_post_args.parse_args()
        ebooks = Ebook.query.filter_by(name=args['name']).first()

        if ebooks :
            return jsonify({'message':'Book is already Available'})
        input=Ebook(name=args['name'],content=args['content'],authors=args['authors'],section_id=args['section_id'])
        db.session.add(input)
        db.session.commit()
        return jsonify({"status":"Success","message":"Book added Succesfully"})
    
class Ebook_remove_Api(Resource):
    @jwt_required()   
    @marshal_with(resource_field)

    def put(self,ebook_id):
        args =ebooks_put_args.parse_args()

        ebook_f = Ebook.query.filter_by(ebook_id = ebook_id).first()

        if not ebook_f:
            abort( 404, message="book doesnt exist" )
        
        if args['name']:
            ebook_f.name = args['name']

        if args['content'] :
            ebook_f.content = args['content']

        db.session.commit()
        return jsonify ({"satus":"Success"})
    
    @marshal_with(resource_field)
    def delete(self,ebook_id):
        ebook_f = Ebook.query.filter_by(ebook_id = ebook_id).first()

        if not ebook_f:
            return jsonify({ 'message':'this book doesnot exist'}),404
        db.session.delete(ebook_f)
        db.session.commit()

        return jsonify({'Status':'Success'}),200 
