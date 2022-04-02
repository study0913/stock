from flask import Blueprint, request
from app import db
from sqlalchemy import or_, and_
import json
from app.models import Stock, AlchemyEncoder
from app.myget_stock import get_stock_info, get_rt_hq

stock = Blueprint("stock", __name__)


#  分页获取股票信息
@stock.route('/list', methods=['get', 'post'])
def get_by_page():
    info = request.get_data()
    if info:
        info = json.loads(info)
        page = info['page']
        pagesize = info['pagesize']
        search = info['search']
        print(info)
    else:
        page = 1
        pagesize = 10
    if search:
        search_filter = {
            or_(
                Stock.stock_code.like('%{search}%'.format(search=search)),
                Stock.stock_name.like('%{search}%'.format(search=search)),
            )
        }
        stocks = Stock.query.filter(*search_filter).paginate(page, pagesize)
    else:
        stocks = Stock.query.paginate(page, pagesize)
        print(json.dumps(stocks.items, cls=AlchemyEncoder))
    res = {'page': stocks.page, 'pages': stocks.pages, 'data': json.dumps(stocks.items, cls=AlchemyEncoder)}
    return res


#  分页获取股票实时行情信息
@stock.route('/list_hq', methods=['get', 'post'])
def get_hq_by_page():
    info = request.get_data()
    if info:
        info = json.loads(info)
        page = info['page']
        pagesize = info['pagesize']
        search = info['search']
        print(info)
    else:
        page = 1
        pagesize = 10
    if search:
        search_filter = {
            or_(
                Stock.stock_code.like('%{search}%'.format(search=search)),
                Stock.stock_name.like('%{search}%'.format(search=search)),
            )
        }
        stocks = Stock.query.filter(*search_filter).paginate(page, pagesize)
    else:
        stocks = Stock.query.paginate(page, pagesize)
    stock_data = []
    for stock1 in stocks.items:
        stock_code = stock1.stock_code
        hq = get_rt_hq(stock_code)
        stock1.rt_price = hq[3]
        stock1.rate =hq[2]
        stock1.range = hq[7]
        stock_data.append(stock1)
    print(stock_data)
    res = {'page': stocks.page, 'pages': stocks.pages, 'data': json.dumps(stock_data, cls=AlchemyEncoder)}
    return res


#  根据stock_code从网上抓取最新信息
@stock.route('/get_stock_web', methods=['get', 'post'])
def get_stock_web():
    param = request.get_data()
    if param:
        param = json.loads(param)
        stock_code = param['stock_code']
        stock_info = get_stock_info(stock_code)
        return json.dumps(stock_info)
    return '网上抓取股票信息失败！！！', 400


#  根据stock_code从数据库反馈记录信息
@stock.route('/get_stock', methods=['get', 'post'])
def get_stock():
    param = request.get_data()
    if param:
        param = json.loads(param)
        stock_code = param['stock_code']
        stock1 = Stock.query.filter(Stock.stock_code == stock_code).first()
        print(json.dumps(stock1, cls=AlchemyEncoder))
        return json.dumps(stock1, cls=AlchemyEncoder)
    return '参数传递失败！！！', 400


#  接收form数据，添加股票
@stock.route('/add_stock', methods=['post'])
def add_stock():
    param = request.get_data()
    if param:
        param = json.loads(param)
        print(param)
        if param['stock_id']:
            Stock.query.filter(Stock.id == param['stock_id']).update({"stock_code": param['stock_code'],
                                                                      "stock_name": param['stock_name'],
                                                                      "stock_type": param['stock_type'],
                                                                      "issue_price": param['issue_price'],
                                                                      "reg_capital": param['reg_capital'],
                                                                      "address": param['address'],
                                                                      "company_name": param['company_name'],
                                                                      "company_brief": param['company_brief'],
                                                                      "total_value": param['total_value'],
                                                                      "pe_ratio": param['pe_ratio'],
                                                                      "current_price": param['current_price']})
            db.session.commit()
        else:
            stock1 = Stock()
            stock1.stock_code = param['stock_code']
            stock1.stock_name = param['stock_name']
            stock1.stock_type = param['stock_type']
            stock1.issue_price = param['issue_price']
            stock1.reg_capital = param['reg_capital']
            stock1.address = param['address']
            stock1.company_name = param['company_name']
            stock1.company_brief = param['company_brief']
            stock1.total_value = param['total_value']
            stock1.pe_ratio = param['pe_ratio']
            stock1.current_price = param['current_price']
            try:
                db.session.add(stock1)
                db.session.commit()
                return '用户添加成功！'
            except Exception as e:
                db.session.rollback()
                return '用户数据有问题，添加失败！！！'
    return '参数获取失败，数据添加不成功', 400


#  删除股票
@stock.route('/delete', methods=['post'])
def delete():
    param = request.get_data()
    if param:
        param = json.loads(param)
        print(param)
        stock_code = param['stock_code']
        stock2 = Stock.query.filter(Stock.stock_code == stock_code).first()
        db.session.delete(stock2)
        db.session.commit()
        return '股票删除成功！'
    return '股票删除失败！！！', 400


#  同步所有股票行情数据,此方法为后台行情任务，系统户用时执行，每天下午15点执行一次
@stock.route('/update_hq')
def update_hq():
    print('股票行情后台更新')
    stocks = Stock.query.all()
    for stock1 in stocks:
        stock_code = stock1.stock_code
        hq = get_rt_hq(stock_code)
        stock1.current_price = hq[3]
        # print(stock1.stock_name,stock1.current_price)

    db.session.commit()
