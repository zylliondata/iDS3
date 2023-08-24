FROM registry.zylliondata.local/centos:7-python-3.8.13
# base image: centos7 + python3.8.13

WORKDIR /opt/app
ENV HOME /opt/app
ADD . /opt/app

RUN rm -rf .idea && rm -rf __pycache__ && chmod -R 777 /opt/app && yum install gcc-c++ -y &&  \
    pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

USER 1001
EXPOSE 8080

CMD ["python3", "main.py"]