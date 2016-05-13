# -*- coding: utf-8 -*-

from flask import Blueprint,render_template,request,redirect, url_for, session,flash
from myaccount.models import FinanceTags,FinanceBook
from myaccount import db

finTag = Blueprint('fintag',__name__)


@finTag.route("/tagList",methods=["GET"])
def tagList():
	tagList = FinanceTags.query.filter_by(userId=session.get("userId")).order_by(FinanceTags.tagType).all()
	return render_template("finTagList.html",tagList=tagList)

@finTag.route("/saveFinTag",methods=["POST"])
def saveFinTag():
	id = request.form.get("id")
	userId = session.get("userId")
	tagName = request.form.get("tagName")
	tagComments = request.form.get("tagComments")
	tagTypeId = request.form.get("tagType")
	if(id):
		currentTag = FinanceTags.query.get(id)
		currentTag.tagName = tagName
		currentTag.tagType = tagTypeId
		currentTag.tagComments = tagComments
	else:
		newTag = FinanceTags(tagTypeId,tagName,tagComments,userId)
		db.session.add(newTag)
	db.session.flush()
	flash("success")
	return redirect(url_for(".tagList"))

@finTag.route("/delTag",methods=["GET"])
def delTag():
	id = request.args.get("id")
	if(id):
		currentTag = FinanceTags.query.get(id)
		db.session.delete(currentTag)
	db.session.flush()
	return redirect(url_for(".tagList"))

