from flask import Blueprint, request, flash, session
from app import db
import json
from hashlib import md5
from sqlalchemy import or_, and_
from app.models import User, AlchemyEncoder

user = Blueprint("user", __name__)


#  用户清单
@user.route('/list', methods=['get', 'post'])
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
                User.user_name.like('%{search}%'.format(search=search)),
                User.email.like('%{search}%'.format(search=search)),
                User.mobile_phone.like('%{search}%'.format(search=search)),
            )
        }
        users = User.query.filter(*search_filter).paginate(page, pagesize)
    else:
        users = User.query.paginate(page, pagesize)
    res = {'page': users.page, 'pages': users.pages, 'data': json.dumps(users.items, cls=AlchemyEncoder)}
    return res


#  用户删除
@user.route('/delete', methods=['post'])
def delete_by_id():
    param = request.get_data()
    if param:
        param = json.loads(param)
        print(param)
        user_id = param['id']
        user1 = User.query.filter(User.id == user_id).first()
        res = db.session.delete(user1)
        db.session.commit()
        return '用户删除成功！'
    return '用户删除失败！！！', 400


#  重置密码
@user.route('/reset', methods=['post'])
def reset_password():
    param = request.get_data()
    if param:
        param = json.loads(param)
        print(param)
        user_id = param['id']
        password = param['password']
        user1 = User.query.filter(User.id == user_id).first()
        user1.password = md5(password.encode('utf8')).hexdigest()
        db.session.commit()

        return '密码重置成功！'
    return '密码重置失败！！！', 400


#  添加用户
@user.route('/add_user', methods=['post'])
def add_user():
    param = request.get_data()
    if param:
        param = json.loads(param)
        user_name = param['user_name']
        user2 = User.query.filter(User.user_name == user_name).first()
        if user2:
            return '用户已存在，不能添加重复用户！！！', 400
        print(param)
        user1 = User()
        user1.user_name = param['user_name']
        user1.password = md5('password'.encode('utf8')).hexdigest()
        user1.email = param['email']
        user1.mobile_phone = param['mobile_phone']
        user1.user_type = param['user_type']
        try:
            db.session.add(user1)
            db.session.commit()
            return '用户添加成功！'
        except Exception as e:
            db.session.rollback()
            return '用户数据有问题，添加失败！！！', 400
    flash("前后端参数传递错误，请联系系统员解决")
    return "前后端参数传递错误，请联系系统员解决", 400


#  根据ID获取用户信息
@user.route('/get_by_id', methods=['get', 'post'])
def get_by_id():
    param = request.get_data()
    if param:
        param = json.loads(param)
        print(param)
        user_id = param['id']
        user1 = User.query.filter(User.id == user_id).first()
        return json.dumps(user1, cls=AlchemyEncoder)
    flash("前后端参数传递错误，请联系系统员解决")
    return "前后端参数传递错误，请联系系统员解决", 400


#  根据username获取用户信息
@user.route('/get_by_session', methods=['get', 'post'])
def get_by_session():
    user_name = session.get('username')
    user1 = User.query.filter(User.user_name == user_name).first()
    return json.dumps(user1, cls=AlchemyEncoder)


#  修改用户信息
@user.route('/update', methods=['post'])
def update():
    param = request.get_data()
    if param:
        param = json.loads(param)
        print(param)
        User.query.filter(User.id == param['user_id']).update({"user_name": param['user_name'],
                                                               "status": param['status'],
                                                               "email": param['email'],
                                                               "mobile_phone": param['mobile_phone'],
                                                               "user_type": param['user_type']})
        db.session.commit()

        return '用户修改成功！'
    return '用户修改失败！！！', 400


#  根据user_name获取用户类型
def get_type(user_name):
    user1 = User.query.filter(User.user_name == user_name).first()
    return user1.user_type
