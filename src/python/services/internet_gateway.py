import boto3

REGION = 'ca-central-1'

ec2 = boto3.resource('ec2', REGION)


class InternetGateway:

    @staticmethod
    def create_internet_gateway():
        internet_gateway: ec2.InternetGateway = ec2.create_internet_gateway()
        return internet_gateway

    def attach_internet_gateway_to_vpc(self, vpc_id):
        vpc = ec2.Vpc(vpc_id)
        internet_gateway = self.create_internet_gateway()
        vpc.attach_internet_gateway(InternetGatewayId=internet_gateway.id)
        return internet_gateway
