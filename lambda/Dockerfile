# this dockerfile is meant to deploy this package to lambda
FROM amazonlinux
MAINTAINER "Rex Roof <rexroof@gmail.com>"
WORKDIR /home/lambda

RUN yum install -y python27-pip zip \
    && pip install -U pip \
    && pip install awscli \
    && yum clean all 

# ADD requirements.txt /home/lambda
# RUN pip install -t /home/lambda -r requirements.txt
# ADD lambda_handler.py /home/lambda

ADD build_push.sh /
CMD sh /build_push.sh
