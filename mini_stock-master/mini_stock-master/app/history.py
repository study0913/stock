# from flask import Blueprint, request
# from app import db
# from sqlalchemy import or_, and_
# import json
# from app.models import Stock, AlchemyEncoder
# from app.myget_stock import get_stock_info, get_rt_hq
#
# history = Blueprint("history", __name__)
#
# @history.route('/history', methods=['get','post'])
# def get_code():
#     stock_code = request.get_data()
#     print("enter", stock_code)
