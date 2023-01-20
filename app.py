import json
import logging
import time
import os
import socket
from threading import Thread

import etcd3
import redis

import libs

#
Util_Config = libs.util.Config()
#
# 读取启动配置
CONFIGDATA = json.load(open('./config.json'))
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - ' + \
        CONFIGDATA['appname'] +':Agent:%(module)s:%(lineno)d - %(levelname)s: %(message)s'
)
redisconn = libs.redisc.Connection()
rediscoption = libs.redisc.Option(redisconn)
etcdconn = libs.etcd.Connection(
    CONFIGDATA['etcd']['host'], 
    CONFIGDATA['etcd']['user'],
    CONFIGDATA['etcd']['pwd'],
    CONFIGDATA['etcd']['root'])
etcd_data = libs.etcd.Data(etcdconn)

def EtcdWatchCallback(event):
    logging.info("ETCD Update Event.")
    etcd_config = etcd_data.GetConfig()
    rediscoption = libs.redisc.Option(redisconn)
    sci = Util_Config.EtcdSwitchRedis(etcd_config, CONFIGDATA['config']) 
    rediscoption.SetConfigItem(sci)
    pass

def StartEtcdWatchThread():
    ''' 开始 ETCD 数据监听线程 ''' 
    etcd_data.Watch(CONFIGDATA['etcd']['root'], EtcdWatchCallback)

if __name__ == '__main__': 
    logging.info("Start ConfigAgent... ")
    logging.info("ConfigAgent Appliction Name: " + CONFIGDATA['appname'])
    # 将默认配置导入到 本地Redis 中。
    rediscoption.SetConfigItem(CONFIGDATA['config']['item'])
    logging.info("Import LocalConfig To Redis. ")
    # 获取 ETCD 配置项
    logging.info("Get Etcd Config Data.")
    etcd_config = etcd_data.GetConfig()
    
    # 从 ETCD 下载配置到本地 Redis。
    logging.info("Update Etcd Data To Redis.")
    sci = Util_Config.EtcdSwitchRedis(etcd_config, CONFIGDATA['config']) 
    rediscoption.SetConfigItem(sci)

    # 初始化 ETCD 监听线程
    logging.info("Start ETCD Watch.")
    thread_etcdwatch = Thread(target=StartEtcdWatchThread, args=())
    thread_etcdwatch.start()

    # 监测线程状态
    while True: 
        if not thread_etcdwatch.is_alive(): 
            logging.error("Watch 线程结束，退出进程。")
            exit()
            
        time.sleep(5)

