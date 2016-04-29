# -*- coding: utf-8 -*-

from flask import Blueprint,render_template,request,redirect, url_for, session,flash
from myaccount import db
from myaccount.models import FinanceUsers,FinanceBook,FinanceTags,FinanceTagsType
import hashlib
import time

main = Blueprint('main',__name__)



@main.route('/')
def showMain():
	if session.get("loginId") == None:
		return redirect(url_for(".login"))
	else:
		#获取账本信息
		books = FinanceBook.query.filter_by(userId=session.get("userId")).all()
		
		#取第一个，查分类
		firstBook = books[0]
		tagTypes = FinanceTags.query.filter_by(bookId=firstBook.id).group_by(FinanceTags.tagType).all()
		tagListGroup = []
		for tagTypeEntity in tagTypes:
			tagList = FinanceTags.query.filter_by(tagType=tagTypeEntity.tagType).all()
			tagType = FinanceTagsType.query.filter_by(tagTypeId=tagTypeEntity.tagType).first()
			tagListGroup.append({'tagType':tagType,'tagList':tagList})
		#print(tagListGroup)
		return render_template("main.html",currentDate=time.strftime("%Y-%m-%d", time.localtime()),books=books,tagListGroup=tagListGroup)

@main.route("/login",methods=["POST","GET"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	else:
		email = request.form['email']
		password = request.form['password']
		hash_md5 = hashlib.md5(password.encode('utf-8'))
		print(hash_md5.hexdigest().upper())
		result = FinanceUsers.query.filter_by(loginId=email,password=hash_md5.hexdigest().upper()).first()
		if result == None:
			flash('账号或者密码错误')
			return redirect(url_for('.login'))
		session['loginId'] = result.loginId
		session['userId'] = result.id
		return redirect(url_for(".showMain"))

@main.route("/logout",methods=["POST","GET"])
def logout():
	session['loginId'] = None
	session['userId'] = None
	return redirect(url_for(".login"))
