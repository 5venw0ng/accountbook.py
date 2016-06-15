#!/usr/bin/env python3

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from myaccount import db


class FinanceUsers(db.Model):
	__tablename__='finance_users'
	id = db.Column('id',db.Integer, primary_key=True)
	loginId = db.Column("login_id",db.String(30))
	username = db.Column('user_name',db.String(10))
	password = db.Column('password',db.String(64))
	books = db.relationship('FinanceBook', backref='finUser',lazy='dynamic')
	userTags = db.relationship('FinanceTags', backref='craeteUser',lazy='dynamic')
	userContents = db.relationship('FinanceContent', backref='cntUser',lazy='dynamic')
	def __init__(self,loginId, username, password):
		self.loginId = loginId
		self.username = username
		self.password = password

	def __repr__(self):
		return '<FinanceUsers %r>' % vars(self)

class FinanceBook(db.Model):
	__tablename__='finance_book'
	id = db.Column("id",db.Integer, primary_key=True)
	bookName = db.Column('book_name',db.String(20))
	isDefault = db.Column('is_defalut',db.String(2))
	finContents = db.relationship('FinanceContent', backref='finBook',lazy='dynamic')
	userId = db.Column('user_id',db.Integer,db.ForeignKey('finance_users.id'))

	def __init__(self,bookName,userId,isDefault):
		self.bookName = bookName
		self.userId = userId
		self.isDefault = isDefault

	def __repr__(self):
		return '<financeusers %r>' % vars(self)

class FinanceTagsType(db.Model):
	__tablename__='finance_tags_type'

	tagTypeId = db.Column('tag_type_id',db.String(10),primary_key=True)
	description = db.Column('description',db.String(10))
	tagTypeChildren = db.relationship('FinanceTags', backref='tagTypeEntity',lazy='dynamic')
	def __init__(self,tagTypeId, description):
		self.tagTypeId = tagTypeId
		self.description = description

	def __repr__(self):
		return '<FINANCE_TAGS %r>' % vars(self)


class FinanceTags(db.Model):
	__tablename__='finance_tags'
	id = db.Column("id",db.Integer, primary_key=True)
	tagType = db.Column('tag_type',db.String(10),db.ForeignKey('finance_tags_type.tag_type_id'))
	tagName = db.Column('tag_name',db.String(10))
	tagComments = db.Column('tag_comments',db.String(50))
	userId = db.Column('user_id',db.Integer,db.ForeignKey('finance_users.id'))
	contentTags = db.relationship('ContantTagAssoc', backref='FinTag',lazy='dynamic')
	def __init__(self,tagType, tagName, tagComments,userId):
		self.tagType = tagType
		self.tagName = tagName
		self.tagComments = tagComments
		self.userId = userId

	def __repr__(self):
		return '<FINANCE_TAGS %r>' % vars(self)

class FinanceContent(db.Model):
	__tablename__='finance_content'
	id = db.Column("id",db.Integer, primary_key=True)
	amount = db.Column('amount',db.Float)
	inOut = db.Column('inout',db.String(50))
	craetedDate = db.Column('created_date',db.DateTime)
	billingDate = db.Column('billing_date',db.Date)
	comments = db.Column('comments',db.String(50))
	bookId = db.Column('book_id',db.Integer,db.ForeignKey('finance_book.id'))
	userId = db.Column('user_id',db.Integer,db.ForeignKey('finance_users.id'))
	contentTags = db.relationship('ContantTagAssoc', backref='FinContent',lazy='joined')

	def __init__(self,inOut,amount, billingDate,comments, bookId,userId):
		self.amount = amount
		self.inOut = inOut
		self.billingDate = billingDate
		self.bookId = bookId
		self.comments = comments
		self.userId = userId

	def __repr__(self):
		return '<financecontent %r>' % vars(self)

class ContantTagAssoc(db.Model):
	__tablename__='content_tags_assoc'
	contentId = db.Column('content_id',db.Integer,db.ForeignKey('finance_content.id'),primary_key=True)
	tagId = db.Column('tag_id',db.Integer,db.ForeignKey('finance_tags.id'),primary_key=True)

	def __init__(self,contentId, tagId):
		self.contentId = contentId
		self.tagId = tagId

	def __repr__(self):
		return '<contanttagassoc %r>' % vars(self)