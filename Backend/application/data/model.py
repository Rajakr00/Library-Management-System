from datetime import datetime
current_utc_datetime = datetime.utcnow()
from .database import db

from flask_security import UserMixin, RoleMixin
from sqlalchemy import event
from sqlalchemy import Column, Integer, String, DateTime ,LargeBinary

UserRoles = db.Table('UserRoles',
	                 db.Column('user_id',db.Integer(),db.ForeignKey('user.user_id')),
					 db.Column('role_id',db.Integer(),db.ForeignKey('role.id')))
class Role(db.Model,RoleMixin):
	__tablename__ = 'role'
	id = db.Column(db.Integer(),primary_key=True)
	name = db.Column(db.String(100),unique=True)


class user(db.Model,UserMixin):
	__tablename__ = 'user'
	user_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	user_name = db.Column(db.String(80),nullable=False)
	user_mail = db.Column(db.String,unique=True,nullable = False )
	password = db.Column(db.String,nullable = False)
	admin = db.Column(db.Boolean)
	active = db.Column(db.Boolean)
	fs_uniquifier = db.Column(db.String,unique=True,nullable=False)

	roles = db.relationship('Role',secondary=UserRoles,
		     backref=db.backref('user',lazy='dynamic'))

	# token based authentication

	def __init__(self,user_mail,user_name,password,admin,fs_uniquifier):
		self.user_mail=user_mail
		self.user_name=user_name
		self.password = password
		self.fs_uniquifier = fs_uniquifier
		self.admin=admin

class Section(db.Model):
	__tablename__='Section'
	section_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	section_name =db.Column(db.String(100),nullable=False)
	date_created = db.Column(db.DateTime)
	section_description = db.Column(db.String(200),nullable=True)
	ebook = db.relationship('Ebook',backref='section',lazy=True)

	def __init__(self,section_name,date_created,section_description):
		self.section_name = section_name
		self.date_created=date_created
		self.section_description= section_description

class Ebook(db.Model):
	__tablename__='Ebook'
	ebook_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	name=db.Column(db.String(80),nullable=False)
	content = db.Column(db.String(150))
	authors = db.Column(db.String(180),nullable=False)
	# book_pdf = db.Column(db.LargeBinary)
	
	section_id = db.Column(db.Integer, db.ForeignKey('Section.section_id'),nullable=False)
	# book_issue = db.Relationship('Book_issue',backref='ebook',lazy=True)

	def __init__(self,name,content,authors,section_id):
		self.name=name
		self.content=content
		self.authors=authors
		self.section_id=section_id

class book_issue(db.Model):
	__tablename__ = 'book_issue'
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'), nullable=False)
	ebook_id =db.Column(db.Integer,db.ForeignKey('Ebook.ebook_id',ondelete='CASCADE'),nullable=False)
	status = db.Column(db.String,nullable=False,default='pending')
	issue_date =db.Column(db.DateTime,default=datetime.utcnow)
	return_date=db.Column(db.String)

	# user = db.relationship('User', backref=db.backref('Book_issues', lazy=True))
	# Ebook = db.relationship('eBook', backref=db.backref('Book_issues', lazy=True))

	def __init__(self,user_id,ebook_id,status,issue_date,return_date):
		self.user_id=user_id
		self.ebook_id=ebook_id
		self.status=status
		self.issue_date=issue_date
		self.return_date=return_date