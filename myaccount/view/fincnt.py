# -*- coding: utf-8 -*-

from flask import Blueprint,render_template,request,redirect, url_for, session,flash
from sqlalchemy import desc
from myaccount.models import FinanceContent,ContantTagAssoc
from myaccount import db
import time

fincontent = Blueprint('fincontent',__name__)


@fincontent.route("/savecnt",methods=["POST"])
def savecnt():
	try:
		print(request.form)
		amount = request.form.get("amount")
		bookId = request.form.get("bookId")
		comments = request.form.get("comments")
		selectTag = request.form.getlist("selectTag")
		billingDate = request.form.get("billingDate")
		inOut = request.form.get("inOut")
		newcnt = FinanceContent(inOut,amount,billingDate,comments,bookId,userId=session.get("userId"))
		db.session.add(newcnt)
		db.session.flush()

		for tagId in selectTag:
			newCt = ContantTagAssoc(newcnt.id,tagId)
			db.session.add(newCt)
	except:
		return "发生错误"
	finally:
		return "Y"

@fincontent.route("/loadCurrentDateBill",methods=["GET"])
def loadCurrentDateBill():
	#查询当天的账单
	currentDateBills = FinanceContent.query.filter_by(billingDate=time.strftime("%Y-%m-%d", time.localtime())).order_by(desc(FinanceContent.craetedDate)).all()
	return render_template("currentDateBill.html",currentDateBills=currentDateBills)
