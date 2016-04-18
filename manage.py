#!/usr/bin/env python3

from flask import Flask
from flask_script import Server, Shell, Manager, Command, prompt_bool
from myaccount import view,app,register_blueprints,db,initLogInfo
import myaccount.models


app.debug = True
app.secret_key="test"
manager = Manager(app)

#启动服务器
#manager.add_command("runserver", Server('0.0.0.0',port=5000))

#实例化日志组件
initLogInfo(app)

#注册route蓝图
@manager.command
def runserver():
	register_blueprints(app)
	app.run()

@manager.command
def initdb():
	app.logger.info("开始实例化数据库……")
	db.create_all()

if __name__ == '__main__':
	manager.run()
