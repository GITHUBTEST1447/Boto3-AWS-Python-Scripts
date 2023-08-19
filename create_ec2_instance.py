import boto3

ec2_client = boto3.client('ec2')

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
response = ec2_client.run_instances(**parameters)