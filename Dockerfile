FROM python:3.10.11-bullseye
MAINTAINER xiaowu wangxiaowu950330@foxmail.com
WORKDIR /app
# 安装/配置SSH,Nginx
RUN echo 'deb https://mirrors.aliyun.com/debian/ bullseye main non-free contrib\n\
    deb-src https://mirrors.aliyun.com/debian/ bullseye main non-free contrib\n\
    deb https://mirrors.aliyun.com/debian-security/ bullseye-security main\n\
    deb-src https://mirrors.aliyun.com/debian-security/ bullseye-security main\n\
    deb https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib\n\
    deb-src https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib\n\
    deb https://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib\n\
    deb-src https://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib' \
    > /etc/apt/sources.list \
    && chmod 777 /tmp/ \
    && apt update -y \
    && apt -y install openssh-server nginx \
    && mkdir /var/run/sshd \
    && sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && echo 'root:root' | chpasswd \
    && ssh-keygen -A \
    && ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
# 配置jdk和allure
RUN curl -L https://download.java.net/java/GA/jdk11/13/GPL/openjdk-11.0.1_linux-x64_bin.tar.gz -o /usr/local/src/openjdk11.tar.gz \
    && cd /usr/local/src && tar -zxvf openjdk11.tar.gz  \
    && rm -f openjdk11.tar.gz  \
    && mv jdk* openjdk11  \
    && curl -L https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.22.0/allure-commandline-2.22.0.tgz -o /usr/local/src/allure.tgz \
    && tar -xf /usr/local/src/allure.tgz -C /usr/local/ \
    && mv /usr/local/allure* /usr/local/allure
ENV ALLURE_HOME=/usr/local/allure
ENV JAVA_HOME=/usr/local/src/openjdk11
ENV PATH=$PATH:$JAVA_HOME/bin:$ALLURE_HOME/bin
COPY nginx.conf /etc/nginx/nginx.conf
COPY start.sh ./start.sh
# 下载依赖
COPY requirements.txt ./requirements.txt
RUN chmod +x ./start.sh \
    && pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
ENV IS_SSH=true
COPY . .
# 暴露端口
EXPOSE 22 80 9999
# 启动
CMD ["sh", "start.sh"]
