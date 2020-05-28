from src.python.services.internet_gateway import InternetGateway
from src.python.services.key_pair import KeyPair
from src.python.services.profile_iam import InstanceProfile
from src.python.services.role_iam import InstanceRoleIAM
from src.python.services.route import Route
from src.python.services.route_table import TableRoute
from src.python.services.security_group import SecurityGroup
from src.python.services.subnet import Subnet
from src.python.services.vpc import Vpc


def main():

    vpc_seminaire = Vpc(
        "Name",
        "seminaire_vpc",
        "10.1.0.0/16"
    )

    result_vpc = vpc_seminaire.create_vpc()
    print("VPC ID : " + result_vpc.id)

    internet_gateway_seminaire = InternetGateway()
    result_ig = internet_gateway_seminaire.attach_internet_gateway_to_vpc(result_vpc.id)
    print("Internet Gateway ID : " + result_ig.id)

    route_table_seminaire = TableRoute()
    result_route_table = route_table_seminaire.create_route_table(result_vpc.id)
    print("Route Table ID : " + result_route_table.id)

    route_seminaire = Route(
        "0.0.0.0/0",
        result_ig.id
    )
    route_seminaire.create_route(result_route_table.id)

    subnet_seminaire = Subnet(
        "10.1.10.0/24",
        result_vpc.id
    )
    result_subnet = subnet_seminaire.attach_table_route_to_subnet(result_route_table.id, result_vpc.id)
    print("Public Subnet ID : " + result_subnet.id)

    security_group_seminaire = SecurityGroup(
        "security_group_vpc_jt",
        "allow rdp connection",
        result_vpc.id,
        "0.0.0.0/0",
        "tcp",
        3389
    )
    result_security_group = security_group_seminaire.authorize_ingress_traffic()
    print("Security Group ID : " + result_security_group.group_id)

    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    default_path = "/"
    role_name_seminaire = "ec2_instance_role_jt"

    iam_role_seminaire = InstanceRoleIAM(
        default_path,
        role_name_seminaire,
        assume_role_policy_document,
        "Role instance EC2",
        3600,
        "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
    )
    iam_role_seminaire.create_role()
    iam_role_seminaire.attach_role_policy()

    instance_profile_seminaire = InstanceProfile(
        "ec2-instance-profile-jt",
        default_path,
        role_name_seminaire
    )
    instance_profile_seminaire.create_instance_profile()
    instance_profile_seminaire.attach_role_to_profile()

    key_pair_seminaire = KeyPair("jt_key_pair")
    result_key_pair = key_pair_seminaire.create_key_pair()
    print("Nom de la Key Pair : " + result_key_pair.name)


if __name__ == "__main__":
    main()
