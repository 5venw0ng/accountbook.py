#!/usr/bin/env python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from myaccount import db

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1:3306/myfinance'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#db = SQLAlchemy(app)

class FinanceUsers(db.Model):
	__tablename__='FINANCE_USERS'
	id = db.Column('ID',db.Integer, primary_key=True)
	loginId = db.Column("LOGIN_ID",db.String(30))
	username = db.Column('USER_NAME',db.String(10))
	password = db.Column('PASSWORD',db.String(64))
	books = db.relationship('FinanceBook', backref='finUser',lazy='dynamic')

	def __init__(self,loginId, username, password):
		self.loginId = loginId
		self.username = username
		self.password = password

	def __repr__(self):
		return '<FinanceUsers %r>' % vars(self)

class FinanceBook(db.Model):
	__tablename__='FINANCE_BOOK'
	id = db.Column("ID",db.Integer, primary_key=True)
	bookName = db.Column('BOOK_NAME',db.String(20))
	finContents = db.relationship('FinanceContent', backref='finBook',lazy='dynamic')
	bookTags = db.relationship('FinanceTags', backref='finBook',lazy='dynamic')
	userId = db.Column('USER_ID',db.Integer,db.ForeignKey('FINANCE_USERS.ID'))

	def __init__(self,bookName,userId):
		self.bookName = bookName
		self.userId = userId

	def __repr__(self):
		return '<FinanceUsers %r>' % vars(self)

class FinanceTagsType(db.Model):
	__tablename__='FINANCE_TAGS_TYPE'

	tagTypeId = db.Column('TAG_TYPE_ID',db.String(10),primary_key=True)
	description = db.Column('DESCRIPTION',db.String(10))
	tagTypeChildren = db.relationship('FinanceTags', backref='tagType',lazy='dynamic')
	def __init__(self,tagTypeId, description):
		self.tagTypeId = tagTypeId
		self.description = description

	def __repr__(self):
		return '<FINANCE_TAGS %r>' % vars(self)


class FinanceTags(db.Model):
	__tablename__='FINANCE_TAGS'
	id = db.Column("ID",db.Integer, primary_key=True)
	tagType = db.Column('TAG_TYPE',db.String(10),db.ForeignKey('FINANCE_TAGS_TYPE.TAG_TYPE_ID')))
	tagName = db.Column('TAG_NAME',db.String(10))
	tagComments = db.Column('TAG_COMMENTS',db.String(50))
	bookId = db.Column('BOOK_ID',db.Integer,db.ForeignKey('FINANCE_BOOK.ID')))
	contentTags = db.relationship('ContantTagAssoc', backref='FinTag',lazy='dynamic')
	def __init__(self,tagType, tagName, tagComments):
		self.tagType = tagType
		self.tagName = tagName
		self.tagComments = tagComments

	def __repr__(self):
		return '<FINANCE_TAGS %r>' % vars(self)

class FinanceContent(db.Model):
	__tablename__='FINANCE_CONTENT'
	id = db.Column("ID",db.Integer, primary_key=True)
	amount = db.Column('AMOUNT',db.Float)
	craetedDate = db.Column('CREATED_DATE',db.DateTime)
	billingDate = db.Column('BILLING_DATE',db.Date)
	comments = db.Column('COMMNETS',db.String(50))
	bookId = db.Column('BOOK_ID',db.Integer,db.ForeignKey('FINANCE_BOOK.ID'))
	contentTags = db.relationship('ContantTagAssoc', backref='FinContent',lazy='dynamic')

	def __init__(self,amount, billingDate,comments, bookId):
		self.amount = amount
		self.billingDate = billingDate
		self.bookId = bookId
		self.comments = comments

	def __repr__(self):
		return '<FinanceContent %r>' % vars(self)

class ContantTagAssoc(db.Model):
	__tablename__='CONTENT_TAGS_ASSOC'
	contentId = db.Column('CONTENT_ID',db.Integer,db.ForeignKey('FINANCE_CONTENT.ID'),primary_key=True)
	tagId = db.Column('TAG_ID',db.Integer,db.ForeignKey('FINANCE_TAGS.ID'),primary_key=True)

	def __init__(self,contentId, tagId):
		self.contentId = contentId
		self.tagId = tagId

	def __repr__(self):
		return '<ContantTagAssoc %r>' % vars(self)

if __name__ == '__main__':
	pass
	#financeUser = FinanceUsers('zhuce@wyl.im','admin','fucku')
	#db.session.add(financeUser)
	#db.session.commit()
	#app.run(debug=True)
	#tagList = FinanceTags.query.all()
	#print(tagList)

	#finBook = FinanceBook('默认账本',1)
	#db.session.add(finBook)
	#db.session.commit()

	#content = FinanceContent(-19.8,datetime.now(),'测试添加一条数据',finBook.id)
	#db.session.add(content)
	#db.session.commit()

	#book = FinanceBook.query.filter_by(id='1').first()
	#print(book.finUser)

	#contentTag = ContantTagAssoc(1,2)
	#db.session.add(contentTag)
	#db.session.commit()

	#content = FinanceContent.query.filter_by(id='1').first()
	#print(content.finBook)

	#contentTag = ContantTagAssoc.query.filter_by(contentId='1').first()
	#print(contentTag.FinTag.tagName)
	#print(contentTag.FinContent.comments)
