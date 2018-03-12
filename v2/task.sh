#!/bin/sh

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
if [ "$1" = "stop" ] ; then
    /apps/python/python2/bin/supervisorctl -c supervisord.conf stop $2

elif [ "$1" = "restart" ]; then
    /apps/python/python2/bin/supervisorctl -c supervisord.conf restart $2

elif [ "$1" = "-d" ]; then
    /apps/python/python2/bin/supervisord -c /apps/web/wm-b2c/v1/supervisord.conf

elif [ "$1" = "start" ]; then
    /apps/python/python2/bin/supervisorctl -c supervisord.conf start $2

else
    echo "usage: $0 -d|start|stop|restart"
fi