import boto3

REGION = 'ca-central-1'

iam = boto3.resource('iam', REGION)
client_iam = boto3.client('iam', REGION)


class InstanceProfile:
    def __init__(self, profile_name, path, role_name):
        self.profile_name = profile_name
        self.path = path
        self.role_name = role_name

    def create_instance_profile(self):
        instance_profile: iam.InstanceProfile = iam.create_instance_profile(
            InstanceProfileName=self.profile_name,
            Path=self.path
        )
        return instance_profile

    def attach_role_to_profile(self):
        client_iam.add_role_to_instance_profile(
            InstanceProfileName=self.profile_name,
            RoleName=self.role_name
        )