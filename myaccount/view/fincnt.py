# -*- coding: utf-8 -*-

from flask import Blueprint,render_template,request,redirect, url_for, session,flash,jsonify
from sqlalchemy import desc,and_
from myaccount.models import FinanceContent,ContantTagAssoc
from myaccount import db
import time

fincontent = Blueprint('fincontent',__name__)


@fincontent.route("/savecnt",methods=["POST"])
def savecnt():
	try:
		print(request.form)
		amount = request.form.get("amount")
		bookId = session['defbookId']
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


#查询当天的账单
@fincontent.route("/loadCurrentDateBill",methods=["GET"])
def loadCurrentDateBill():
	userId = session.get("userId")
	currentDateBills = FinanceContent.query.filter(and_(FinanceContent.craetedDate.startswith(time.strftime('%Y-%m-%d', time.localtime())),FinanceContent.userId==userId,FinanceContent.bookId==session['defbookId'])).order_by(desc(FinanceContent.craetedDate)).all()
	return render_template("currentDateBill.html",currentDateBills=currentDateBills)

#查询所有账单，实际上默认查询3天内的
@fincontent.route("/allData",methods=["GET"])
def allData():
	userId = session.get("userId")
	cntList = FinanceContent.query.filter_by(userId=userId,bookId=session['defbookId']).order_by(desc(FinanceContent.craetedDate)).all()
	return render_template("contentList.html",cntList=cntList)

#删除一个账单
@fincontent.route("/delCnt/<id>",methods=["GET"])
def delCnt(id):
	if id == None:
		return "错误，找不到id"
	else:
		assocs = ContantTagAssoc.query.filter_by(contentId=id).delete()
		db.session.flush()

		cnt = FinanceContent.query.get(id)
		db.session.delete(cnt)
	return jsonify(isSuccess="Y")
