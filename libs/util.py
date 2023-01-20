import logging

class Config:
    ''' 配置信息类 '''

    def EtcdSwitchRedis(self, etcd_config, config_file_data):
        ''' 
        将ETCD数据转换为 Redis 数据 
        '''
        redata = {}
        for i in etcd_config: 
            if i in config_file_data['etcdmap']: 
                redata[config_file_data['etcdmap'][i]] = etcd_config[i]
                logging.info(
                    'ETCD 映射: ' + str(i) + \
                        '    Redis对应键: ' + str(config_file_data['etcdmap'][i]))
            else:
                logging.warn('ETCD 存在一个没有映射 Redis的键: ' + str(i))
        return redata