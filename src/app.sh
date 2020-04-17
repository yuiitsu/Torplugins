#!/bin/sh

#/apps/python/python2/bin/gunicorn -k tornado -w 1 -b 0.0.0.0:9000 index:app >> /apps/web/logs/wmb2c.log &
#/apps/python/python2/bin/gunicorn -k tornado -w 1 -b 0.0.0.0:9000 index:app
#SH_DIR=$(dirname $(which $0))
#. $SH_DIR/app_env.sh

DATA_VAR_DIR=/apps/data/wmb2c
LOGS_DIR=/apps/logs/wmb2c
ROOT_DIR=/apps/web/wm-b2c

BASE_DIR=$ROOT_DIR/v1
CONF_DIR=$ROOT_DIR/conf

###########################################################
mkdir -p $DATA_VAR_DIR
#mkdir -p $LOGS_DIR/run

###################################
# OPTIONS=$OPTIONS" -c $CONF_DIR/nginx.conf"

############################################################
echo "Please use task.sh."
exit 1
if [ "$1" = "stop" ] ; then
    kill -QUIT `cat $DATA_VAR_DIR/gunicorn.pid`

elif [ "$1" = "restart" ]; then
    kill -HUP `cat $DATA_VAR_DIR/gunicorn.pid`

elif [ "$1" = "start" ]; then
    # $BASE_DIR/sbin/nginx $OPTIONS
    /apps/python/python3/bin/gunicorn -c /apps/web/wm-b2c/v1/app.conf.py index:app -D --capture-output --enable-stdio-inheritance

elif [ "$1" = "test" ]; then
    #$BASE_DIR/sbin/nginx -t $OPTIONS
    echo "test"

else
    echo "usage: $0 start|stop|restart"
fi
