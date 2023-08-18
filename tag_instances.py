import boto3

def tag_instances():
    # Initialize the Boto3 EC2 client
    ec2_client = boto3.client('ec2')

    # Describe instances to filter only running Linux instances
    response = ec2_client.describe_instances(
        Filters=[
            {'Name': 'image-id', 'Values': ['ami-08a52ddb321b32a8c']},
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
                {'Key': 'Operating System', 'Value': 'Linux'}
                # Add more tags as needed, using the above format
            ]
        )

        return len(instance_ids)
    else:
        return 0

if __name__ == '__main__':
    tagged_count = tag_instances()
    print(f"Tagged {tagged_count} EC2 instance(s) running Linux.")