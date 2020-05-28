from typing import List
import boto3
from botocore.exceptions import ClientError

REGION = 'ca-central-1'

client_ec2 = boto3.client('ec2', REGION)
ec2 = boto3.resource('ec2', REGION)
client_iam = boto3.client('iam', REGION)


class InstanceEC2:
    def __init__(self, image_id, instance_type, count, subnet_id, device_index, security_group_id,
                 public_ip, monitoring, key_pair_name, profile_name):
        self.image_id = image_id
        self.instance_type = instance_type
        self.count = count
        self.subnet_id = subnet_id
        self.device_index = device_index
        self.security_group_id = security_group_id
        self.public_ip = public_ip
        self.monitoring = monitoring
        self.key_pair_name = key_pair_name
        self.profile_name = profile_name

    def create_instances(self):
        instance: List[ec2.Instance] = ec2.create_instances(
            ImageId=self.image_id,
            InstanceType=self.instance_type,
            MaxCount=self.count,
            MinCount=self.count,
            NetworkInterfaces=[{
                'SubnetId': self.subnet_id,
                'DeviceIndex': self.device_index,
                'Groups': [self.security_group_id],
                'AssociatePublicIpAddress': self.public_ip
            }],
            Monitoring={
                'Enabled': self.monitoring
            },
            KeyName=self.key_pair_name
        )
        instance[0].wait_until_running()
        return instance

    @staticmethod
    def print_message(message, current_state_message, previous_state_message):
        print(message)
        print(current_state_message)
        print(previous_state_message)

    def stop_instances(self, instance_id: str):
        try:
            stop_response = client_ec2.stop_instances(InstanceIds=[instance_id])
            instance_ec2 = ec2.Instance(instance_id)
            instance_ec2.wait_until_stopped()
            stop_instance = stop_response.get('StoppingInstances')
            current_state = stop_instance[0].get('CurrentState')
            previous_state = stop_instance[0].get('PreviousState')
            self.print_message("---------- Arrêter instance ------------",
                               'État après : ' + current_state.get('Name'),
                               'État avant : ' + previous_state.get('Name')
                               )
        except ClientError:
            raise

    def arn_profile(self):
        response_instance_profile_name = client_iam.get_instance_profile(
            InstanceProfileName=self.profile_name,
        )
        result_instance_profile = response_instance_profile_name.get('InstanceProfile')
        result_arn: str = result_instance_profile.get('Arn')
        return result_arn

    def attach_profile_to_instance(self, instance_id: str):
        profile_arn: str = self.arn_profile()

        attach_profile_to_instance = client_ec2.associate_iam_instance_profile(
            IamInstanceProfile={
                'Arn': profile_arn
            },
            InstanceId=instance_id,
        )

        state = attach_profile_to_instance.get('IamInstanceProfileAssociation')
        result = state.get('State')
        return result

    def start_instances(self, instance_id: str):
        try:
            start_response = client_ec2.start_instances(InstanceIds=[instance_id])
            instance_ec2 = ec2.Instance(instance_id)
            instance_ec2.wait_until_running()
            start_instance = start_response.get('StartingInstances')
            current_state = start_instance[0].get('CurrentState')
            previous_state = start_instance[0].get('PreviousState')
            self.print_message(
                "---------- Démarrer instance ------------",
                'État après : ' + current_state.get('Name'),
                'État avant : ' + previous_state.get('Name')
            )
        except ClientError:
            raise

    def terminate_instances(self, instance_id: str):
        try:
            instance_ec2 = ec2.Instance(instance_id)
            terminate_response = instance_ec2.terminate()
            instance_ec2.wait_until_terminated()
            terminate_instance = terminate_response.get('TerminatingInstances')
            current_state = terminate_instance[0].get('CurrentState')
            previous_state = terminate_instance[0].get('PreviousState')
            self.print_message(
                "---------- Détruire instance ------------",
                'État après : ' + current_state.get('Name'),
                'État avant : ' + previous_state.get('Name')
            )
        except ClientError:
            raise
