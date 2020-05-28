# Bienvenue à l'atelier sur le séminaire de Boto3

#### https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html

#### https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html

## PARTIE 1 - Script Python (atelier1.py)

### Étape 1 - Création d'un VPC (Virtual Private Cloud)

#### Client
- Accès aux services AWS de bas niveau
- Générer depuis le service de description AWS
- Expose Client botocore au développeur
- Toutes les opérations des services AWS sont supporté par Client

#### Resource
- Accès de haut niveau aux objets orientés de l'API
- Générer depuis la resource de description AWS
- Utilise des identifiants et des attributs
- Expose les sous-ressources et les collections des ressources d'AWS
- N'offre pas une couverture à 100% d'API des services AWS

import boto3\
import json

REGION = 'ca-central-1'

resource = boto3.resource('ec2', REGION)\
client = boto3.client('ec2', REGION)\
iam = boto3.client('iam', REGION)

vpc = resource.create_vpc(CidrBlock='10.1.0.0/16')\
vpc.create_tags(Tags=[{"Key": "Name", "Value": "seminaire_vpc"}])\
vpc.wait_until_available()\
print("VPC ID : " + vpc.id)

### Étape 2 - Création d'une Passerelle Internet

internet_gateway = resource.create_internet_gateway()\
print("Internet Gateway ID : " + internet_gateway.id)

### Étape 3 - Attacher une Passerelle Internet au VPC

#### La Passerelle Internet permet de fournit une cible dans vos tables de routage VPC pour le trafic routable sur Internet

vpc.attach_internet_gateway(InternetGatewayId=internet_gateway.id)

### Étape 4 - Création d'une table de routage

route_table = vpc.create_route_table()

### Étape 5 - Création d'une route dans la table de routage
route = route_table.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=internet_gateway.id)\
print("Route Table ID : " + route_table.id)

### Étape 6 - Création d'un sous-réseau public
#### Différence entre un sous-réseau public et une sous-réseau privé
#### Privé
    - Un sous-réseau privé aura seulement une adresse IP privée.
    - Il va configurer la route 0.0.0.0/0 à une Paserrelle NAT qui sera dans un sous-réseau public.
    - Il pourrait avoir aucune route vers 0.0.0.0/0 pour être complémentement privé, sans aucune communication entre lui et l'Internet.
#### Public
    - Un sous-réseau public va avoir une route 0.0.0.0/0 vers la Paserelle Internet.
    - Nécessite une adresse IP public pour communiquer avec l'Internet.
    
public_subnet = vpc.create_subnet(CidrBlock='10.1.10.0/24', VpcId=vpc.id)\
print("Public Subnet ID : " + public_subnet.id)

### Étape 7 - Associer la table routage au sous-réseau public
route_table.associate_with_subnet(SubnetId=public_subnet.id)

### Étape 8 - Création d'un Security Group pour l'instance EC2 (Firewall)
#### Changer VOTRE_NOM par votre nom
security_group = resource.create_security_group(\
    GroupName='security_group_vpc_VOTRE_NOM', Description='allow rdp connection', VpcId=vpc.id)

### Étape 9 - Autoriser le trafic entrant à partir du port 3389
security_group.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=3389, ToPort=3389)\
print("Secury Group ID : " + security_group.group_id)

### Étape 10 - Création du rôle IAM pour l'instance EC2
#### Changer VOTRE_NOM par votre nom
assume_role_policy_document = {\
    "Version": "2012-10-17",\
    "Statement": [\
        {\
            "Sid": "",\
            "Effect": "Allow",\
            "Principal": {\
                "Service": "ec2.amazonaws.com"\
            },\
            "Action": "sts:AssumeRole"\
        }\
    ]\
}\

iam_role = iam.create_role(\
    Path='/',\
    RoleName='ec2_instance_role_VOTRE_NOM',\
    AssumeRolePolicyDocument=json.dumps(assume_role_policy_document),\
    Description='Role instance EC2',\
    MaxSessionDuration=3600\
)

### Étape 11 - Attacher la police AmazonEC2FullAccess au IAM Rôle
#### Changer VOTRE_NOM par votre nom
iam.attach_role_policy(\
    RoleName='ec2_instance_role_VOTRE_NOM',\
    PolicyArn='arn:aws:iam::aws:policy/AmazonEC2FullAccess'\
)

### Étape 12 - Création d'un profile d'instance
#### Changer VOTRE_NOM par votre nom
instance_profile = iam.create_instance_profile(\
    InstanceProfileName='ec2-instance-profile-VOTRE_NOM',\
    Path='/'\
)

### Étape 13 - Ajouter IAM Rôle au profile d'instance
#### Changer VOTRE_NOM par votre nom
add_role_to_profile = iam.add_role_to_instance_profile(\
    InstanceProfileName='ec2-instance-profile-VOTRE_NOM',\
    RoleName='ec2_instance_role_VOTRE_NOM'\
)

### Étape 14 - Création d'une Key Pair
#### Changer VOTRE_NOM par votre nom
response = resource.create_key_pair(KeyName='VOTRE_NOM_key_pair')\
print(response.name)

#### *Important de garder Subnet Public ID et Security Group ID*
#### *Vous pouvez maintenant lancer le script*

## PARTIE 2 - Script Python (atelier2.py)
### Étape 15 - Création d'une instance EC2
#### Trouver une image AMI aec AWS CLI, grâce à la commande suivante :
#### aws ec2 describe-images --owners self amazon --filters "Name=name,Values=Windows_Server-2019-English-Full-Base*"
#### Changer ID_IMAGE par l'id de l'AMI choisit
#### Changer PUBLIC_SUBNET_ID par l'id du sous-réseau privé
#### Changer SECURITY_GROUP_ID par l'id du groupe de sécurité
#### Changer VOTRE_NOM par votre nom

import boto3\
from botocore.exceptions import ClientError

REGION = 'ca-central-1'

resource = boto3.resource('ec2', REGION)\
client = boto3.client('ec2', REGION)\
iam = boto3.client('iam', REGION)

instance = resource.create_instances(\
    ImageId='ID_IMAGE',\
    InstanceType='t2.micro',\
    MaxCount=1,\
    MinCount=1,\
    NetworkInterfaces=[{\
        'SubnetId': 'PUBLIC_SUBNET_ID',\
        'DeviceIndex': 0,\
        'Groups': ['SECURITY_GROUP_ID'],\
        'AssociatePublicIpAddress': True\
    }],\
    Monitoring={\
        'Enabled': True\
    },\
    KeyName='VOTRE_NOM_key_pair'\
)\
instance[0].wait_until_running()\
print("Instance ID : " + instance[0].id)

### Étape 16 - Gestion de l'instance EC2

instance_id = instance[0].id\
instance = resource.Instance(instance_id)

### Étape 17 - Arrêter l'instance EC2

try:\
    stop_response = client.stop_instances(InstanceIds=[instance_id])\
    instance.wait_until_stopped()\
    stop_instance = stop_response.get('StoppingInstances')\
    current_state = stop_instance[0].get('CurrentState')\
    previous_state = stop_instance[0].get('PreviousState')\
    print('Arrêter l'instance EC2')\
    print('État après : ' + current_state.get('Name'))\
    print('État avant : ' + previous_state.get('Name'))\
except ClientError as e:\
    raise
    
### Étape 18 - Attacher le profile IAM à l'instance EC2
#### Changer VOTRE_NOM par votre nom
response_instance_profile_name = iam.get_instance_profile(\
    InstanceProfileName='ec2-instance-profile-VOTRE_NOM',\
)\
result_instance_profile = response_instance_profile_name.get('InstanceProfile')\
result_arn: str = result_instance_profile.get('Arn')

attach_profile_to_instance = client.associate_iam_instance_profile(\
    IamInstanceProfile={\
        'Arn': result_arn,\
    },\
    InstanceId=instance_id,\
)\
state = attach_profile_to_instance.get('IamInstanceProfileAssociation')\
result = state.get('State')\
print("IAM Role est " + result + " à l'instance EC2")

### Étape 19 - Démarrer l'instance EC2

try:\
    start_response = client.start_instances(InstanceIds=[instance_id])\
    instance.wait_until_running()\
    start_instance = start_response.get('StartingInstances')\
    current_state = start_instance[0].get('CurrentState')\
    previous_state = start_instance[0].get('PreviousState')\
    print('Démarrer l'instance EC2')\
    print('État après : ' + current_state.get('Name'))\
    print('État avant : ' + previous_state.get('Name'))\
except ClientError as e:\
    raise
    
### Étape 20 - Détruire l'instance EC2

try:\
    terminate_response = instance.terminate()\
    instance.wait_until_terminated()\
    terminate_instance = terminate_response.get('TerminatingInstances')\
    current_state = terminate_instance[0].get('CurrentState')\
    previous_state = terminate_instance[0].get('PreviousState')\
    print('Détruire l'instance EC2')\
    print('État après : ' + current_state.get('Name'))\
    print('État avant : ' + previous_state.get('Name'))\
except ClientError as e:\
    raise
