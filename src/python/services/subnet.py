import boto3

REGION = 'ca-central-1'

ec2 = boto3.resource('ec2', REGION)


class Subnet:

    def __init__(self, range_ip, vpc_id):
        self.range_ip = range_ip
        self.vpc_id = vpc_id

    def create_subnet(self, vpc_id):
        vpc = ec2.Vpc(vpc_id)
        public_subnet: ec2.Subnet = vpc.create_subnet(
            CidrBlock=self.range_ip,
            VpcId=self.vpc_id
        )
        return public_subnet

    def attach_table_route_to_subnet(self, route_table_id, vpc_id):
        vpc = ec2.Vpc(vpc_id)
        public_subnet = self.create_subnet(vpc)
        route_table = ec2.RouteTable(route_table_id)
        route_table.associate_with_subnet(SubnetId=public_subnet.id)
        return public_subnet
