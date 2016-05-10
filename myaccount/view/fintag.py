# -*- coding: utf-8 -*-

from flask import Blueprint,render_template,request,redirect, url_for, session,flash
from myaccount.models import FinanceTags,FinanceBook
from myaccount import db

finTag = Blueprint('fintag',__name__)


@finTag.route("/bookList",methods=["GET"])
def bookList():
	books = FinanceBook.query.filter_by(userId=session.get("userId")).all()

	return render_template("finBookListWithEditTag.html",books=books)

@finTag.route("/tagList/<bookId>",methods=["GET"])
def tagList(bookId):
	book = FinanceBook.query.get(bookId)

	tagList = FinanceTags.query.filter_by(bookId=bookId).order_by(FinanceTags.tagType).all()
	return render_template("finTagList.html",tagList=tagList, book = book)

@finTag.route("/saveFinTag",methods=["POST"])
def saveFinTag():
	id = request.form.get("id")
	bookId = request.form.get("bookId")
	tagName = request.form.get("tagName")
	tagComments = request.form.get("tagComments")
	tagTypeId = request.form.get("tagType")
	if(id):
		currentTag = FinanceTags.query.get(id)
		currentTag.tagName = tagName
		currentTag.tagType = tagTypeId
		currentTag.tagComments = tagComments
	else:
		newTag = FinanceTags(tagTypeId,tagName,tagComments,bookId)
		db.session.add(newTag)
	db.session.flush()
	flash("success")
	return redirect(url_for(".tagList",bookId=bookId))

@finTag.route("/delTag",methods=["GET"])
def delTag():
	id = request.args.get("id")
	bookId = request.args.get("bookId")
	if(id):
		currentTag = FinanceTags.query.get(id)
		db.session.delete(currentTag)
	db.session.flush()
	return redirect(url_for(".tagList",bookId=bookId))

