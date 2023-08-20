import boto3

# This program is intended to be a basic script that will apply a tag of all instances that match a certain AMI ID
# Created by Steffen Pfahnl

def tag_ec2_instances():
    # Initialize ec2_client object
    ec2_client = boto3.client('ec2')

    # Filter instances to only those running specific AMI/OS
    response = ec2_client.describe_instances(
        Filters=[
            {'Name': 'image-id', 'Values': ['ami-08a52ddb321b32a8c']}, # Modify AMI-ID here as needed
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    # Extract instance IDs
    instance_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])


    # Apply tags to instances
    if instance_ids:
        ec2_client.create_tags(
            Resources=instance_ids,
            Tags=[
                {'Key': 'Operating System', 'Value': 'Linux'} # Modify tag here as needed
                # Add more tags as needed, using the above format
            ]
        )

        return len(instance_ids)
    else:
        return 0

if __name__ == '__main__':
    tagged_count = tag_ec2_instances()
    print(f"Tagged {tagged_count} EC2 instance(s) running Linux.")