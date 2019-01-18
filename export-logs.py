import boto3
from datetime import datetime, timezone


client = boto3.client('logs')

# response = client.create_export_task(
#     taskName='logs-to-s3-task',
#     logGroupName='SOAPlog',
#     fromTime=1547510400000,
#     to=1547769600000,
#     destination='lamark-log-stream',
#     destinationPrefix='SOAP-logs'
# )
fromTime = datetime(2019,1,17,0,0,0,0).timestamp()
to = datetime(2019,1,17,23,59,59).timestamp()
print(fromTime, int(to))

dt_object = datetime.fromtimestamp(1547769599)
print(dt_object)

response = client.describe_export_tasks(
    taskId='68c766ae-a1a9-4488-947c-f0fdf8f8e88e'
)

print("Response of logs-to-S3 lambda function: ", response)


# 1547683200000
# 1547769599000
# 1547769599.0