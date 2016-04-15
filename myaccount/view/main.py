# -*- coding: utf-8 -*-

from flask import Blueprint,render_template,request,redirect, url_for, session
from myaccount import db
from myaccount.models import FinanceUsers

main = Blueprint('main',__name__)



@main.route('/')
def showMain():
	if session.get("userInfo") == None:
		return redirect(url_for(".login"))
	return "首页"

@main.route("/login",methods=["POST","GET"])
def login():
	if request.method == "GET":
		return render_template("login.html")
