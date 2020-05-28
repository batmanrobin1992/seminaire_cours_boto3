import boto3

REGION = 'ca-central-1'

ec2 = boto3.resource('ec2', REGION)


class TableRoute:

    @staticmethod
    def create_route_table(vpc_id):
        vpc = ec2.Vpc(vpc_id)
        route_table: ec2.RouteTable = vpc.create_route_table()
        return route_table
