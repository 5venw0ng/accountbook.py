# -*- coding: utf-8 -*-

from flask import Blueprint,render_template,request,redirect, url_for, session,flash
from myaccount import db,app
from myaccount.models import FinanceUsers,FinanceBook,FinanceTags,FinanceTagsType,FinanceContent
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
		tagTypes = FinanceTags.query.filter_by(userId=session.get("userId")).group_by(FinanceTags.tagType).all()
		tagListGroup = []
		for tagTypeEntity in tagTypes:
			tagList = FinanceTags.query.filter_by(tagType=tagTypeEntity.tagType).all()
			tagType = FinanceTagsType.query.filter_by(tagTypeId=tagTypeEntity.tagType).first()
			tagListGroup.append({'tagType':tagType,'tagList':tagList})

		return render_template("main.html",currentDate=time.strftime("%Y-%m-%d", time.localtime()),books=books,tagListGroup=tagListGroup)

@main.route("/login",methods=["POST","GET"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	else:
		email = request.form['email']
		password = request.form['password']
		hash_md5 = hashlib.md5(password.encode('utf-8'))
		
		result = FinanceUsers.query.filter_by(loginId=email,password=hash_md5.hexdigest().upper()).first()
		if result == None:
			flash('账号或者密码错误')
			return redirect(url_for('.login'))

		#取出默认的账本
		defbook = FinanceBook.query.filter_by(userId=result.id,isDefault='Y').first()
		if defbook == None:
			defbook = FinanceBook.query.filter_by(userId=result.id).first()

		session['loginId'] = result.loginId
		session['userId'] = result.id
		session['defbookId'] = defbook.id
		return redirect(url_for(".showMain"))

@main.route("/logout",methods=["POST","GET"])
def logout():
	session['loginId'] = None
	session['userId'] = None
	return redirect(url_for(".login"))

@main.route("/changePasswod",methods=["POST","GET"])
def changePasswod():
	if request.method == "POST":
		userId = session.get("userId")
		oldpassword = request.form.get("oldpassword")
		password = request.form.get("password")
		confirmPwd = request.form.get("confirmPassword")

		currentUser = FinanceUsers.query.get(userId)
		hash_md5 = hashlib.md5(oldpassword.encode('utf-8'))
		oldpassword = hash_md5.hexdigest().upper()
		if currentUser.password == oldpassword:
			if password == confirmPwd:
				hash_md5 = hashlib.md5(password.encode('utf-8'))
				password = hash_md5.hexdigest().upper()
				currentUser.password = password
				db.session.add(currentUser)
				db.session.flush()
				flash('密码修改成功，请重新登录')
				return redirect(url_for(".logout"))
			else:
				flash('新密码2次输入不一样')
		else:
			flash('原始密码错误！')
	return render_template("changePasswod.html")

@main.route("/register",methods=["POST","GET"])
def register():
	if request.method == "GET":
		return render_template("register.html")
	else:
		loginId = request.form.get("loginId")
		userName = request.form.get("userName")
		password = request.form.get("password")
		confirmPwd = request.form.get("confirmPassword")
		if( login==None or userName==None or password==None or confirmPwd==None):
			flash('账号、昵称、密码都不能为空')
			return render_template("register.html",loginId=loginId,userName=userName)
		if password!=confirmPwd:
			flash('2次密码输入不一致')
			return render_template("register.html",loginId=loginId,userName=userName)
		hash_md5 = hashlib.md5(password.encode('utf-8'))
		password = hash_md5.hexdigest().upper()
		result = FinanceUsers.query.filter_by(loginId=loginId).first()
		if result == None:
			newuser = FinanceUsers(loginId,userName,password)
			db.session.add(newuser)
			db.session.flush()

			#默认添加一个账本
			newBook = FinanceBook('默认账本',newuser.id)
			db.session.add(newBook)
			db.session.flush()

			session['loginId'] = newuser.loginId
			session['userId'] = newuser.id

			flash('注册成功，自动创建一个账本')
			return redirect(url_for("financeBook.bookList"))
			
		else:
			flash('%s 已经存在' % loginId)
			return render_template("register.html",userName=userName)

@app.after_request
def call_after_request_callbacks(response):
	db.session.commit()
	return response
