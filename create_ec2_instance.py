import boto3

# Create ec2 client object
ec2_client = boto3.client('ec2')

# Define dictionary containing parameters for EC2 instance creation
parameters = {
    'ImageId' : 'ami-08a52ddb321b32a8c',
    'MinCount' : 1,
    'MaxCount' : 1,
    'InstanceType' : 't2.micro',
    'KeyName' : 'PythonTest',
    'SecurityGroupIds' : ['sg-029bfbd37a3d6564c'],
    'SubnetId' : 'subnet-020fae177a10d0d92',
    'TagSpecifications' : [{
            
            'ResourceType' : 'instance',
            'Tags' : [{'Key' : 'Name', 'Value' : 'TEST-PYTHON-1'}]

            }]
}

# API request to create a EC2 instance with the predefined parameters
response = ec2_client.run_instances(**parameters)