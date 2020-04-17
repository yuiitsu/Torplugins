import gevent.monkey
gevent.monkey.patch_all()
import multiprocessing

debug = True
loglevel = 'info'
bind = '0.0.0.0:9000'
pidfile = '/apps/data/wmb2c/gunicorn.pid'
logfile = '/apps/data/wmb2c/debug.log'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'tornado'

x_forwarded_for_header = 'X-FORWARDED-FOR'

errorlog = '/apps/web/logs/gun_error.log'
accesslog = '/apps/web/logs/gun_access.log'