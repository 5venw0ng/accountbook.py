# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/myfinance'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

# 注册蓝图（好像只有route会用这个）
def register_blueprints(app):
	app.logger.info('====register_blueprints')
	from myaccount.view import main
	from myaccount.view import financeBook
	from myaccount.view import fintag
	from myaccount.view import fincnt
	app.register_blueprint(main.main,url_prefix="")
	app.register_blueprint(financeBook.finBook,url_prefix="/finbook")
	app.register_blueprint(fintag.finTag,url_prefix="/fintag")
	app.register_blueprint(fincnt.fincontent,url_prefix="/fincnt")

def initLogInfo(app):
	handler = logging.FileHandler('flask.log')
	logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
	handler.setFormatter(logging_format)
	handler.setLevel(logging.DEBUG)
	app.logger.addHandler(handler)



