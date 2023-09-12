import boto3

# Create API client objects

alb_client = boto3.client('elbv2', region_name='us-east-1')
ec2_client = boto3.client('ec2', region_name='us-east-1')

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
    public_subnets = get_public_subnets(vpc_id)
    print(public_subnets)

    #alb_response = alb_client.create_load_balancer(Name='Python ALB', Type='application', Subnets=subnetIDs)

if __name__ == "__main__":
    vpc_id = input()
    create_alb(vpc_id)