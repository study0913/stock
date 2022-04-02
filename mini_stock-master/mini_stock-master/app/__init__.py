from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from app.scheduler import SchedulerConfig
import pymysql
pymysql.install_as_MySQLdb()



app = Flask(__name__)
# 加载配置文件
app.config.from_object(Config)


# 为实例化的flask引入定时任务配置
app.config.from_object(SchedulerConfig())
# db绑定app
db = SQLAlchemy(app)



from app import models
