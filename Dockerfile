
#   docker build ./ -t  meidongauto-docker.pkg.coding.net/itsm/private/configagent:0.1

#   docker push meidongauto-docker.pkg.coding.net/itsm/private/configagent:0.1



FROM rockylinux
#
# 环境变量
ENV LANG C.UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
#
# YUM
RUN sed -e 's|^mirrorlist=|#mirrorlist=|g' \
    -e 's|^#baseurl=http://dl.rockylinux.org/$contentdir|baseurl=https://mirrors.aliyun.com/rockylinux|g' \
    -i.bak /etc/yum.repos.d/Rocky-*.repo && dnf install epel-release -y
#
# 基础环境
RUN yum install python36 python36-* gcc -y 
RUN groupadd --gid 5000 py \
  && useradd --home-dir /home/py --create-home --uid 5000 \
    --gid 5000 --shell /bin/sh --skel /dev/null py \
  && yum install passwd -y && echo 'yaokai' | passwd --stdin root
#
# 应用环境
WORKDIR /usr/app
COPY ./ /usr/app
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple --upgrade pip
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt
USER py
ENTRYPOINT ["python3","app.py"]


