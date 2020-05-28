import json
import boto3

REGION = 'ca-central-1'

iam = boto3.resource('iam', REGION)
client_iam = boto3.client('iam', REGION)


class InstanceRoleIAM:
    def __init__(self, path, role_name, assume_policy, description, max_session_duration, police_arn):
        self.path = path
        self.role_name = role_name
        self.assume_policy = assume_policy
        self.description = description
        self.max_session_duration = max_session_duration
        self.police_arn = police_arn

    def create_role(self):
        iam_role: iam.Role = iam.create_role(
            Path=self.path,
            RoleName=self.role_name,
            AssumeRolePolicyDocument=json.dumps(self.assume_policy),
            Description=self.description,
            MaxSessionDuration=self.max_session_duration
        )
        return iam_role

    def attach_role_policy(self):
        client_iam.attach_role_policy(
            RoleName=self.role_name,
            PolicyArn=self.police_arn
        )