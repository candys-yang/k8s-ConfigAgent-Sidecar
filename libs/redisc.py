'''
Redis 操作库
'''
import logging
import redis

class Connection:
    def __init__(self) -> None:
        self.redisc = redis.Redis(host='127.0.0.1', decode_responses=True)

class Option:
    def __init__(self, conn:Connection) -> None:
        self.redisc = conn.redisc
        pass

    def SetConfigItem(self, data:dict):
        ''' 
        将数据更新到 Redis 上。 
        
        Args:
            data:{
                键: 值
            }
        '''
        for i in data: 
            logging.info("Update Redis Keys: " + str(i))
            self.redisc.set(i, data.get(i))

        