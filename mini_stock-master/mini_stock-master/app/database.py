from app import db
from hashlib import md5
import models

#  先清空数据库
db.drop_all()
#  重新构建数据结构
db.create_all()
#  添加管理员记录
user = models.User(user_name='root', password=md5('root'.encode('utf8')).hexdigest(), user_type='M')
db.session.add(user)
db.session.commit()
