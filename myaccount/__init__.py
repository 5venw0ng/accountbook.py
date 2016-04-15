# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1:3306/myfinance'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# 注册蓝图
def register_blueprints(app):
    from myaccount.view import main
    from myaccount.view import financeBook

    app.register_blueprint(main.main,url_prefix="")
    app.register_blueprint(financeBook.finBook,url_prefix="/finbook")

