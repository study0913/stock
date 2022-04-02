from flask_apscheduler import APScheduler  # 引入APScheduler
from app.stock import update_hq


# 任务配置类
class SchedulerConfig(object):
    JOBS = [
        {
            'id': 'update_hq',  # 任务id
            'func': '__main__:update_hq',  # 任务执行程序
            'args': None,  # 执行程序参数
            'trigger': 'interval',  # 任务执行类型，定时器
            'minutes ': 5,  # 任务执行时间，单位秒
        }
    ]
