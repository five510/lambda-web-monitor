## Build

1. Running docker container with 
```
$ sudo docker build ./ --no-cache -t lambda-deployment
$ sudo docker run --rm \
-e AWS_ACCESS_KEY_ID="" \
-e AWS_SECRET_ACCESS_KEY="" \
-it lambda-deployment bash
```

2. deploy it

```
$ aws cloudformation package \
  --s3-bucket ${YOUR_S3_BUCKET} \
  --template-file lambda.yml \
  --output-template-file packaged-template.yml 

$ aws cloudformation deploy \
  --template-file packaged-template.yml \
  --stack-name goto-new-stack-web-monitor \
  --parameter-overrides \
  LambdaExecutionRole=arn:aws:iam::${ACCOUNT_NUMBER}:role/LambdaExecutionRole 
```

## Monitor metrics

- Status code
- response time