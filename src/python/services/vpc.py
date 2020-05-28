import boto3

REGION = 'ca-central-1'

ec2 = boto3.resource('ec2', REGION)


class Vpc:

    def __init__(self, key, value, range_ip):
        self.key = key
        self.value = value
        self.range_ip = range_ip

    def create_vpc(self):
        vpc: ec2.Vpc = ec2.create_vpc(CidrBlock=self.range_ip)
        vpc.create_tags(Tags=[{"Key": self.key, "Value": self.value}])
        vpc.wait_until_available()
        return vpc
