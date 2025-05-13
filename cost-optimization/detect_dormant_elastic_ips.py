"""
Detects and releases dormant Elastic IPs in AWS:
    This AWS Lambda function identifies all Elastic IP addresses that are not associated with any EC2 instances or network interfaces (i.e., dormant) and releases them to avoid unnecessary costs.
    Returns:
        dict: A response containing the status code and information about released IPs
            - statusCode (int): HTTP status code (200 for success)
            - body (str): Message indicating how many IPs were released and their addresses
"""
import boto3

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    
    # Describe all Elastic IPs
    addresses = ec2_client.describe_addresses()
    released = []

    for addr in addresses['Addresses']:
        # If not associated with any instance or network interface
        if 'InstanceId' not in addr and 'NetworkInterfaceId' not in addr:
            try:
                ec2_client.release_address(AllocationId=addr['AllocationId'])
                released.append(addr['PublicIp'])
                print(f'Released Elastic IP: {addr["PublicIp"]}')

            except Exception as exception:
                print(f'Error releasing {addr["PublicIp"]}: {exception}')
    return {
        'statusCode': 200,
        'body': f'Released {len(released)} Elastic IPs: {released}'
    }
