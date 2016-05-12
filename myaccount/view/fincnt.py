# -*- coding: utf-8 -*-

from flask import Blueprint,render_template,request,redirect, url_for, session,flash
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
		newcnt = FinanceContent(inOut,amount,billingDate,comments,bookId)
		db.session.add(newcnt)
		db.session.flush()

		for tagId in selectTag:
			newCt = ContantTagAssoc(newcnt.id,tagId)
			db.session.add(newCt)
	except:
		return "发生错误"
	finally:
		return "Y"