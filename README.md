# ConfigAgent

基于K8S平台部署应用时使用的 边车容器，用于应用程序的注册中心。

以下文档 Agent 即 ConfigAgent 的代称。


## 配置

### Config.json 说明

```json

{
    "appname": "应用名称",   
    "etcd":{
        "host": ["ETCD服务器:端口"],
        "user": "ETCD用户", 
        "pwd": "ETCD密码", 
        "root": "ETCD数据的根目录"
    },
    "config":{
        // itsm 里的键值会转换为 redis 的 kv，键值和 Redis 里的一致。
        "item":{
            "redis键":"键值"
        },
        // etcd映射，etcdmap里的键为 ETCD 的键，值为 Redis 的键
        // 示例：   TOKENKEY 是ETCD里的键， itsmoauth:TOKENKEY 是Redis的键。
        //         etcd 里 TOKENKEY 的值 = Redis 里 itsmoauth:TOKENKEY 的值。
        "etcdmap":{
            "TOKENKEY": "itsmoauth:TOKENKEY"
        }
    }
}


```


### K8S 应用配置

    config.py 是 Agent 的启动配置文件。
    在 K8S 平台下，可通过挂载 ConfigMap 来实现配置信息控制。

容器: 
```yaml


volumes:
    - name: appname-config-volumes
        configMap:
        name: appname-config
        defaultMode: 420
containers:
    - name: configagent
        image: meidongauto-docker.pkg.coding.net/itsm/private/agentconfig:0.1
        volumeMounts: 
            - name: appname-config-volumes
            mountPath: /usr/app
            subPath: config.json

```

configmap:
``` yaml

kind: ConfigMap
apiVersion: v1
metadata:
  name: appname-config
data:
  config.json: |
    {
    "appname": "应用名称",   
    "etcd":{
        "host": ["ETCD服务器:端口"],
        "user": "ETCD用户", 
        "pwd": "ETCD密码", 
        "root": "ETCD数据的根目录"
    },
    "config":{
        "item":{
            "redis键":"键值"
        },
        "etcdmap":{
            "ETCD键": "Redis键"
        }
    }
}

```

