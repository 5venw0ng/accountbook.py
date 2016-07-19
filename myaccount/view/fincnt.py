# -*- coding: utf-8 -*-

from flask import Blueprint,render_template,request,redirect, url_for, session,flash,jsonify
from sqlalchemy import desc,and_
from myaccount.models import FinanceContent,ContantTagAssoc,FinanceTags,FinanceTagsType
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
@fincontent.route("/allData",methods=["GET","POST"])
def allData():
	userId = session.get("userId")

	query = FinanceContent.query
	query = query.filter(FinanceContent.userId==userId)
	query = query.filter(FinanceContent.bookId==session['defbookId'])
	cntList = query.order_by(desc(FinanceContent.billingDate)).all()

	tempQuery = ContantTagAssoc.query.join(FinanceContent)
	tempQuery = tempQuery.filter(ContantTagAssoc.tagId=='3')
	tempQuery = tempQuery.filter(FinanceContent.id==ContantTagAssoc.contentId)
	tempQuery = tempQuery.filter(and_(FinanceContent.billingDate >= '2016-05-12',FinanceContent.billingDate <= '2016-05-13'))

	tempList = tempQuery.all()
	reqTags = request.form.getlist('selectTag')
	tags = [tag for tag in reqTags if tag!=u'']

	if tags != None and len(tags)>0:
		print("00000000====")
	
	tagTypes = FinanceTags.query.filter_by(userId=session.get("userId")).group_by(FinanceTags.tagType).all()
	tagListGroup = []
	for tagTypeEntity in tagTypes:
		tagList = FinanceTags.query.filter_by(tagType=tagTypeEntity.tagType).all()
		tagType = FinanceTagsType.query.filter_by(tagTypeId=tagTypeEntity.tagType).first()
		tagListGroup.append({'tagType':tagType,'tagList':tagList})

	return render_template("contentList.html",cntList=cntList,tagListGroup=tagListGroup,tempList=tempList)

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
