import boto3

ec2_client = boto3.client('ec2')

def vpc_exists(vpc_id):
    try:
        response = ec2_client.describe_vpcs(VpcIds=[vpc_id])
        if response and 'Vpcs' in response and len(response['Vpcs']) > 0:
            return True
        else:
            return False
    except ec2_client.exceptions.ClientError as e:
        if "InvalidVpcID.NotFound" in str(e):
            return False
        else:
            raise

def create_vpc(region_name, cidr_block):

    # Create a ec2 client object and initialize a empty VPC
    # Gather the VPC id, and use it to add a nametag to the VPC

    vpc_response = ec2_client.create_vpc(CidrBlock=cidr_block)
    vpc_id = vpc_response['Vpc']['VpcId']
    ec2_client.create_tags(Resources=[vpc_id], Tags=[{'Key': 'Name', 'Value': 'Python_VPC'}])

    # Create 4 subnets and gather their IDs

    subnet_response_1 = ec2_client.create_subnet(CidrBlock='10.0.1.0/24', VpcId=vpc_id)
    subnet_response_2 = ec2_client.create_subnet(CidrBlock='10.0.2.0/24', VpcId=vpc_id)
    subnet_response_3 = ec2_client.create_subnet(CidrBlock='10.0.3.0/24', VpcId=vpc_id)
    subnet_response_4 = ec2_client.create_subnet(CidrBlock='10.0.4.0/24', VpcId=vpc_id)

    subnet_1_id = subnet_response_1['Subnet']['SubnetId']
    subnet_2_id = subnet_response_2['Subnet']['SubnetId']
    subnet_3_id = subnet_response_3['Subnet']['SubnetId']
    subnet_4_id = subnet_response_4['Subnet']['SubnetId']

    # Create a internet gateway and route table
    # Attach default route from route table to IGW

    igw_response = ec2_client.create_internet_gateway()
    igw_id = igw_response['InternetGateway']['InternetGatewayId']
    ec2_client.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)

    route_table_response=ec2_client.create_route_table(VpcId=vpc_id)
    route_table_id = route_table_response['RouteTable']['RouteTableId']
    ec2_client.create_route(RouteTableId=route_table_id, GatewayId=igw_id, DestinationCidrBlock='0.0.0.0/0')

    # Associate subnets with the route table specified

    ec2_client.associate_route_table(SubnetId=subnet_1_id, RouteTableId=route_table_id)
    ec2_client.associate_route_table(SubnetId=subnet_2_id, RouteTableId=route_table_id)


    # Return the IDs of each instance
    
    return {
        'VPC_ID': vpc_id,
        'Subnet_1': subnet_1_id,
        'Subnet_2': subnet_2_id,
        'Subnet_3': subnet_3_id,
        'Subnet_4': subnet_4_id,
        'IGW_ID': igw_id,
        'Route_Table_ID': route_table_id
    }

if __name__ == "__main__":
    returnValue = create_vpc('us-east-1', '10.0.0.0/16')
    
    if vpc_exists(str(returnValue['VPC_ID'])):
        print("VPC succesfully created")
    else:
        print("VPC creation failed")