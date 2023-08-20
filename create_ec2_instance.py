import boto3

# This program is intended to be a basic script to create a EC2 instance, it requires certain information (Security Group, SubnetID, Instance Type, AMI ID)
# Created by Steffen Pfahnl

# Create ec2 client object
ec2_client = boto3.client('ec2')

# Declare variables for details about EC2 creation
securityGroup = 'sg-029bfbd37a3d6564c'
subnetId = 'subnet-020fae177a10d0d92'
instanceType = 't2.micro'
imageID = 'ami-08a52ddb321b32a8c'

# Define dictionary containing parameters for EC2 instance creation
parameters = {
    'ImageId' : imageID,
    'MinCount' : 1,
    'MaxCount' : 1,
    'InstanceType' : instanceType,
    'KeyName' : 'PythonTest',
    'SecurityGroupIds' : [securityGroup],
    'SubnetId' : subnetId,
    'TagSpecifications' : [{
            
            'ResourceType' : 'instance',
            'Tags' : [{'Key' : 'Name', 'Value' : 'TEST-PYTHON-1'}]

            }]
}

# API request to create a EC2 instance with the pre-defined parameters
response = ec2_client.run_instances(**parameters)