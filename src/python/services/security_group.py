import boto3

REGION = 'ca-central-1'

ec2 = boto3.resource('ec2', REGION)


class SecurityGroup:
    def __init__(self, group_name, description, vpc_id, range_ip, protocol, port):
        self.group_name = group_name
        self.description = description
        self.vpc_id = vpc_id
        self.range_ip = range_ip
        self.protocol = protocol
        self.port = port

    def create_security_group(self):
        security_group: ec2.SecurityGroup = ec2.create_security_group(
            GroupName=self.group_name,
            Description=self.description,
            VpcId=self.vpc_id
        )
        return security_group

    def authorize_ingress_traffic(self):
        security_group = self.create_security_group()
        security_group.authorize_ingress(
            CidrIp=self.range_ip,
            IpProtocol=self.protocol,
            FromPort=self.port,
            ToPort=self.port
        )
        return security_group
