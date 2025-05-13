# NOTE:
# - This lambda function is intended to be triggred by 'Amazon Event Bridge' via the respective IAM account
# - It checks for EBS volumes in the 'available' state, which means they are unattached and not in use by any EC2 instance and then deletes them.
# - No owner tag is required; all unattached volumes older than 30 days will be deleted.
# - OS: ubuntu

import boto3
from datetime import datetime, timezone

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    days_threshold = 30
    now = datetime.now(timezone.utc)

    # Get all EBS volumes in 'available' state
    response = ec2_client.describe_volumes(Filters=[{
        'Name': 'status',
        'Values': ['available']
    }])

    unused_volumes = []
    for vol in response['Volumes']:
        create_time = vol['CreateTime']
        age_days = (now - create_time).days
        
        if age_days > days_threshold:
            unused_volumes.append(vol['VolumeId'])

    # Delete unused volumes
    for vol_id in unused_volumes:
        try:
            ec2_client.delete_volume(VolumeId = vol_id)
            print(f'Deleted volume: {vol_id}')

        except Exception as exception:
            print(f'Error deleting {vol_id}: {exception}')

    return {
        'statusCode': 200,
        'body': f'Deleted {len(unused_volumes)} unused EBS volumes.'
    }
