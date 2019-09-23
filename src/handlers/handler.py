import requests
import os
import boto3
from botocore.exceptions import ClientError
import json
import datetime
import time
import utils
logger = utils.get_logger()

@utils.logging_handler
def monitor_handler(event,context) -> dict:
    url = event['url']
    response = requests.get(url)
    cloudwatch_upload(url,response)
    return {}

@utils.logging_handler
def cron_handler(event,context) -> dict:
    ssm = boto3.client('ssm')
    ssm_parameter_name = os.environ['SSM_PRAMETER_NAME']
    response = ssm.get_parameters(
        Names=[
            ssm_parameter_name,
        ]
    )
    external_urls = response['Parameters'][0]['Value'].split(',')
    function_name = os.environ['WEB_MONITOR_FUNCTION_ARN'].split(':')[-1]
    lambda_client = boto3.client('lambda')
    for url in external_urls:
        try:
            event = {
                'url': url
            }
            lambda_client.invoke(
                FunctionName=function_name,
                InvocationType="Event",
                Payload=json.dumps(event)
            )
            logger.info('Complete invoke lambda function for {}'.format(url))
        except Exception as e:
            logger.warning(e)
    return {}

def cloudwatch_upload(url,response) -> bool:
    cw_client = boto3.client('cloudwatch')
    time_elapsed = response.elapsed.total_seconds()
    starus_code = response.status_code
    response = cw_client.put_metric_data(
        Namespace='ExternalUrls',
        MetricData=[
            {
                'MetricName': 'status_code',
                'Dimensions': [
                    {
                        'Name': 'url',
                        'Value': url
                    }
                ],
                'Value': starus_code,
                'Unit': 'None'
            },
            {
                'MetricName': 'response_time',
                'Dimensions': [
                    {
                        'Name': 'url',
                        'Value': url
                    }
                ],
                'Value': time_elapsed,
                'Unit': 'None'
            }
        ]
    )
    return True

if __name__ == "__main__":
    event = {
        'url': 'https://google.com'
    }
    monitor_handler(event,{})