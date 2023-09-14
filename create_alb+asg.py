import boto3

# Create API client objects

alb_client = boto3.client('elbv2', region_name='us-east-1')
ec2_client = boto3.client('ec2', region_name='us-east-1')
asg_client = boto3.client('autoscaling', region_name='us-east-1')

# Function to gather public subnets from specified VPC

def get_public_subnets(vpc_id, region_name='us-east-1'):
    # Gather information about all subnets in specified VPC
    response = ec2_client.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    subnets = response['Subnets']

    # Check which subnets are public

    public_subnets = []
    for subnet in subnets: # For each subnet in the VPCs total subnets
        subnet_id = subnet['SubnetId'] # Gather the subnet ID
        route_tables_response = ec2_client.describe_route_tables(Filters=[{'Name': 'association.subnet-id', 'Values': [subnet_id]}]) # Gather all route tables associated with that subnet ID
        for route_table in route_tables_response['RouteTables']: # For each route table in that list
            for route in route_table['Routes']: # for each route in that route table
                if 'GatewayId' in route and route['GatewayId'].startswith('igw-'): # Check if that route is to a IGW
                    public_subnets.append(subnet_id) # If so, add it to the public subnets list
                    break

    return public_subnets

# Function to create ALB
def create_alb(vpc_id):

    # Get public subnets from helper
    public_subnets = get_public_subnets(vpc_id)
    
    # Create Security Group for ALB
    response = ec2_client.create_security_group(GroupName='PYTHON-ALB-SG', Description='SG created for Python ALB', VpcId=vpc_id)
    security_group_id = response['GroupId']
    ec2_client.create_tags(Resources=[security_group_id],Tags=[{'Key': 'Name', 'Value': 'PYTHON-ALB-SG'}])
    ec2_client.authorize_security_group_ingress(GroupId=security_group_id, IpProtocol='tcp', CidrIp='0.0.0.0/0', FromPort=80, ToPort=80)

    # Create Load Balancer
    response = alb_client.create_load_balancer(Name='PYTHON-ALB', Subnets=public_subnets, SecurityGroups=[security_group_id], Scheme='internet-facing', Type='application')
    load_balancer_arn = response['LoadBalancers'][0]['LoadBalancerArn']

    # Create Target Group and Listener for ALB
    response = alb_client.create_target_group(Name='PYTHON-ASG-TG', Protocol='HTTP', Port=80, VpcId=vpc_id)
    target_group_arn = response['TargetGroups'][0]['TargetGroupArn']
    alb_client.create_listener(LoadBalancerArn=load_balancer_arn, Protocol='HTTP', Port=80, DefaultActions=[{'Type': 'forward', 'TargetGroupArn': target_group_arn}])
    
    return {
    "SecurityGroupId": security_group_id,
    "LoadBalancerArn": load_balancer_arn,
    "TargetGroupArn": target_group_arn
    }

def create_asg(vpc_id, lb_security_group_id):

    # Create Security Group for the ASG's launch configuration
    response = ec2_client.create_security_group(GroupName='PYTHON-ASG-SG', Description='SG created for Python ASG', VpcId=vpc_id)
    security_group_id = response['GroupId']
    ec2_client.create_tags(Resources=[security_group_id],Tags=[{'Key': 'Name', 'Value': 'PYTHON-ASG-SG'}])
    ec2_client.authorize_security_group_ingress(GroupId=security_group_id, IpPermissions=[{
                                                                                            'IpProtocol': 'tcp',
                                                                                            'FromPort': 0,
                                                                                            'ToPort': 65535,
                                                                                            'UserIdGroupPairs': [{'GroupId': lb_security_group_id}]
                                                                                            }])
    # Create Launch Configuration
    response = ec2_client.create_launch_template(
    LaunchTemplateName='PYTHON-LT',
    VersionDescription='Initial version',
    LaunchTemplateData = {
        'InstanceType': 't2.micro',
        'SecurityGroupIds': [security_group_id],
        'ImageId': 'ami-0f844a9675b22ea32'
    })

    # Create Auto Scaling Group
    response = asg_client.create_auto_scaling_group(
        AutoScalingGroupName='PYTHON-ASG',
        LaunchTemplate={'LaunchTemplateName': 'PYTHON-LT', 'Version': '1'},
        MinSize=2,
        MaxSize=4,
        DesiredCapacity=2,
        VPCZoneIdentifier = ','.join(get_public_subnets(vpc_id)),
        AvailabilityZones=['us-east-1a', 'us-east-1b']
    )

if __name__ == "__main__":
    vpc_id = input("Input VPC ID: ")
    response = create_alb(vpc_id)
    lb_security_group_id = response["SecurityGroupId"]
    create_asg(vpc_id, lb_security_group_id)