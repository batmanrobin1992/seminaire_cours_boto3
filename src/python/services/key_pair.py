import boto3

REGION = 'ca-central-1'

ec2 = boto3.resource('ec2', REGION)


class KeyPair:
    def __init__(self, key_name):
        self.key_name = key_name

    def create_key_pair(self):
        key_pair: ec2.KeyPair = ec2.create_key_pair(KeyName=self.key_name)
        return key_pair
