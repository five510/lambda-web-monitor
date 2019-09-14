## Build

```
aws cloudformation package \
  --template-file lambda.yml \
  --s3-bucket s3bucket \
  --output-template-file packaged.yml
```

