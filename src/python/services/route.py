import json
import boto3

REGION = 'ca-central-1'

ec2 = boto3.resource('ec2', REGION)


class Route:

    def __init__(self, destination, gateway_id):
        self.destination = destination
        self.gateway_id = gateway_id

    def create_route(self, route_table_id):
        route_table = ec2.RouteTable(route_table_id)
        route: ec2.Route = route_table.create_route(
            DestinationCidrBlock=self.destination,
            GatewayId=self.gateway_id
        )
        return route
