# -*- coding: utf-8 -*-

from flask import Blueprint,render_template,request,redirect, url_for, session,flash
from myaccount import db
from myaccount.models import FinanceUsers
import hashlib

main = Blueprint('main',__name__)



@main.route('/')
def showMain():
	if session.get("loginId") == None:
		return redirect(url_for(".login"))
	else:
		return render_template("main.html")

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
		return redirect(url_for(".showMain"))
		
