# 任务配置类
class SchedulerConfig(object):
    JOBS = [
        {
            'id': 'update_hq',  # 任务id，股票行情更新
            'func': '__main__:update_hq',  # 任务执行程序
            'args': None,  # 执行程序参数
            'trigger': 'cron',                            # 指定任务触发器 cron
            'day_of_week': 'mon-fri',              # 每周1至周5下午15：00点即股票交易结束执行
            'hour': 15,
            'minute': 0
        }
    ]

    JOBS = [
        {
            'id': 'update_earning',  # 任务id，更新帐户持仓收益
            'func': '__main__:get_all_earning',  # 任务执行程序
            'args': None,  # 执行程序参数
            'trigger': 'cron',                            # 指定任务触发器 cron
            'day_of_week': 'mon-fri',              # 每周1至周5下午15：10点即股票交易结束执行
            'hour': 15,
            'minute': 5
        }
    ]

    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
