from src.python.services.instance_ec2 import InstanceEC2


def main():
    instance_seminaire = InstanceEC2(
        'ami-014f55f965f51c865',
        't2.micro',
        1,
        'subnet-0f6611829141b6f8e',
        0,
        'sg-0f29dbf8841556942',
        True,
        True,
        'jt_key_pair',
        'ec2-instance-profile-jt'
    )
    result_instance = instance_seminaire.create_instances()
    instance_id = result_instance[0].id
    print("Instance EC2 ID : " + instance_id)
    instance_seminaire.stop_instances(instance_id)
    result_status = instance_seminaire.attach_profile_to_instance(instance_id)
    print("IAM Role est " + result_status + " à l'instance EC2")
    instance_seminaire.start_instances(instance_id)
    instance_seminaire.terminate_instances(instance_id)


if __name__ == "__main__":
    main()
