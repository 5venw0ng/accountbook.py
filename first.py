#!/usr/bin/env python3

import mysql.connector

class Student(object):


	def aMethod(name):
		print("hello world!,my name is %s"%name)

	def doubleNum(number,n):
		total = 0
		while n > 1:
			total = ( number * number ) if total==0 else (total * number)
			n = n - 1
		return total

	def getData():
		conn = mysql.connector.connect(user="root",password="root",host="127.0.0.1",database="bluemountain")
		cursor = conn.cursor()
		cursor.execute("SELECT PRODUCT_ID,PRODUCT_NAME FROM PRODUCT WHERE IS_VARIANT='N'")
		result = cursor.fetchall()
		for productid,name in result:
			print("商品ID:%s ,商品名称:%s" % (productid,name))

	#aMethod("Sven")

	#print(doubleNum(3,3))




