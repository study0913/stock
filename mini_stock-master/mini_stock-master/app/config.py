import os


class Config(object):
    """base config"""
    # FLASK_DEBUG = True
    SECRET_KEY = 'secretkey17041904'
    # mysql://username:password@server/db
    DB_URL = 'mysql://root:root@localhost:3306/db'
    SQLALCHEMY_DATABASE_URI = DB_URL

    SQLALCHEMY_TRACK_MODIFICATIONS = False

# import os
#
# DEBUG = True
#
# SECRET_KEY = os.urandom(24)
#
# DIALECT = 'mysql'
# DRIVER = 'mysqldb'
# USENAME = 'root'
# PASSWORD = '17041904'
# HOST = '127.0.0.1'
# PORT = '3306'
# DATABASE = 'db'
# #mysql://username:password@server/db
# DB_URL="{}+{}://{}:{}@{}:{}/{}?charset=utf8".\
#     format(DIALECT,DRIVER,USENAME,PASSWORD,HOST,PORT,DATABASE)
#
# SQLALCHEMY_DATABASE_URI=DB_URL
#
# SQLALCHEMY_TRACK_MODIFICATIONS = False
