import boto3

# This program is intended to be a basic script to create a snapshot of a EC2 instance given it's instance ID
# Created by Steffen Pfahnl

# Create ec2 client object
ec2_client = boto3.client('ec2')

# Function for obtaining volume ID from instance ID
def get_volume_id(instance_id):
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    
    volume_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            for device in instance['BlockDeviceMappings']:
                volume_ids.append(device['Ebs']['VolumeId'])
    return volume_ids

# Inputting instance ID and setting it into function to get volume ID
instance_id = 'i-0a7d3479a1059690e'
volume_id = get_volume_id(instance_id)[0]

# Creating snapshot with the obtained volume ID
response = ec2_client.create_snapshot(VolumeId=volume_id)