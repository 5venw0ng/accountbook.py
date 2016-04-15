# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1:3306/myfinance'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# 注册蓝图（好像只有route会用这个）
def register_blueprints(app):
	app.logger.info('====register_blueprints')
	from myaccount.view import main
	from myaccount.view import financeBook
	app.register_blueprint(main.main,url_prefix="")
	app.register_blueprint(financeBook.finBook,url_prefix="/finbook")

def initLogInfo(app):
	handler = logging.FileHandler('flask.log')
	logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
	handler.setFormatter(logging_format)
	handler.setLevel(logging.DEBUG)
	app.logger.addHandler(handler)



