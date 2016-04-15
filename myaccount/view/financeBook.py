# -*- coding: utf-8 -*-
from flask import Blueprint
from myaccount.models import FinanceBook

finBook = Blueprint('financeBook',__name__)


@finBook.route('/hello')
def showHello():
    return "/hello"


