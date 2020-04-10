import json
import boto3
REGION='eu-west-1'

ssm = boto3.client('ssm',region_name=REGION)
ec2 = boto3.client('ec2',region_name=REGION)

def lambda_handler(event, context):
    
    all_instance_ids = set()
    managed_ids = set()
    non_managed_ids = set()
    
    for reservation in ec2.describe_instances()['Reservations']:
        all_instance_ids.add(reservation['Instances'][0]['InstanceId'])

    for instance in ssm.describe_instance_information()['InstanceInformationList']:
        managed_ids.add(instance['InstanceId'])
    
    non_managed_ids = all_instance_ids.difference(managed_ids)
    
    return {
        'statusCode': 200,
        'body': json.dumps(' '.join(non_managed_ids))
    }