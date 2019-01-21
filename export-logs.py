import boto3
from datetime import datetime, timedelta


client = boto3.client('logs')


def get_date_path():
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    date_path = str(year)+'/'+str(month)+'/'+str(day)
    return date_path


def lambda_handler(event, context):
    response = client.create_export_task(
        taskName='logs-to-s3-task',
        logGroupName=event["logGroupName"],
        fromTime=int(round((datetime.now() - timedelta(days=1)).timestamp() * 1000)),
        to=int(round(datetime.now().timestamp() * 1000)),
        destination='lamark-log-stream',
        destinationPrefix=event["logGroupName"]+'/'+get_date_path()
    )

    print("Response of logs-to-s3 lambda function: " + response['taskId'])
