'''
ETCD 操作类
'''


import time
import logging
import etcd3

class Connection: 
    ''' etcd操作 '''
    def __init__(self, host:list, user:str, password:str, root:str) -> None:
        ''' 
        连接 ETCD 服务器。

        如果所有主机不可用，则抛出异常。
        
        Args:
            host:       etcd主机列表。 ['127.0.0.1:2379', ...]
            user:       etcd用户名
            password:   etcd密码

        '''
        self.client = None
        self.root = root
        for i in host: 
            logging.info("Connection to etcd server " + str(i))
            try:
                etcd = etcd3.client(
                    host= i.rsplit(":")[0], 
                    port= i.rsplit(":")[1], 
                    user= user, 
                    password= password,
                    timeout=10,
                )
                self.client = etcd
                break
            except Exception as e:
                logging.warning("Connection to etcd server fail " + str(i))
        if self.client is None:
            logging.error("Connection to etcd server , All Attempts Failed ")

class System: 
    ''' ETCD 系统信息类 '''
    def __init__(self, Conn:Connection):
        self.conn = Conn
        self.client = Conn.client
        pass

    def Status(self):
        ''' 
        获取 ETCD 状态 
        
        Returns:{
            "size":     数据库大小
            "leader":   主节点名
        }
        '''
        s = self.client.status()
        return {
            "size": s.db_size,
            "leader": s.leader.name,
        }



class Data: 
    ''' ETCD 业务数据类 '''
    def __init__(self, Conn:Connection) -> None:
        self.conn = Conn
        self.client = Conn.client
        self.root = Conn.root
        pass

    def GetConfig(self):
        ''' 
        从 ETCD 获取应用配置 
        
        Returns:    dict，返回 ETCD存储的键值 {key:value} 
                    （key是去掉根目录字符的）
        '''
        v = self.client.get_prefix(self.root + '/')
        redata = {}
        for i in v:
            logging.info("ETCD Config Keys:" + i[1].key.decode())
            _k = str(i[1].key.decode()).replace(self.root + '/',"")
            _v = i[0].decode()
            redata[_k] = _v
        return redata

    def Watch(self, root, callback):
        ''' 监听 ETCD 键值 '''
        watch_id = self.client.add_watch_prefix_callback(
            root + '/', 
            callback
        )
        while watch_id == 0: 
            _t, _m = self.client.get(root + '/test')
            time.sleep(10)
