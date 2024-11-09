import json
from flask import request,jsonify
from flask_restful import Resource,reqparse,abort,fields, marshal_with
from flask_jwt_extended.view_decorators import jwt_required
from datetime import datetime
from application.cache import cache

# importing model from database
from application.data.model import db,Section,Ebook
from application.data.All_data_access import get_all_section

#  post argument 

section_post_args =reqparse.RequestParser()
section_post_args.add_argument('section_name',type=str,required=True)
section_post_args.add_argument('section_description',type=str)


# put argument

section_put_args=reqparse.RequestParser()
section_put_args.add_argument('section_name',type=str,required=True)
section_put_args.add_argument('section_description',type=str)


# decorater for marshal 

resource_field = {
    'section_id':fields.Integer,
    'section_name':fields.String,
    'section_description':fields.String,
    'section_dateTime':fields.DateTime,
    
}
class CreateSectionAPI(Resource):
    @marshal_with(resource_field)
    @jwt_required() 
    def post(resource):
        args = section_post_args.parse_args()
        section = Section.query.filter_by(section_name=args['section_name']).first()

        if section:
            abort(409,message="section already exist")

        input = Section(section_name=args['section_name'],section_description=args['section_description'],date_created=datetime.now())
        db.session.add(input)
        db.session.commit()
        return  ({"status":"Success"})

class AllSectionAPI(Resource):
    @cache.cached(timeout=2)
    @jwt_required()
    def get(Resource):
        section = get_all_section()
        return section
    
class sectionAPI(Resource):
    @jwt_required()

    @marshal_with(resource_field)
    

    def get(self, section_id):
        section = Section.query.filter_by(section_id=section_id).first()
        if not section:
            abort ('404', message="could not found section")
        return section
    def delete(self,section_id):
        section = Section.query.filter_by(section_id=section_id).first()

        if not section:
            return jsonify({ 'message':'this section doesnot exist'}),404
        db.session.delete(section)
        db.session.commit()

        return jsonify({'status':'deleted successfully'},200)
    
    # api for edit section
class sectionEditAPI(Resource):
    @marshal_with(resource_field)
    @jwt_required()

    def put(self,section_id):
        args=section_put_args.parse_args()

        section = Section.query.filter_by(section_id = section_id).first()

        if not section:
            abort( 404, message="section doesnt exist" )
        
        if args['section_name']:
            section.section_name = args['section_name']

        if args['section_description'] :
            section.section_description = args['section_description']

        db.session.commit()

        return ({"status":"Success"})
    

    





