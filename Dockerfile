FROM lambci/lambda:build-python3.7
ENV LANG C.UTF-8
ENV AWS_DEFAULT_REGION ap-northeast-1

WORKDIR /tmp

COPY . .

RUN pip install -r requirements.txt -t /tmp/src/handlers