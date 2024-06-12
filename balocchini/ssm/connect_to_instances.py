import boto3
import argparse
import subprocess
import sys

def list_ssm_instances(profile=None):
    session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    ssm_client = session.client('ssm')
    ec2_client = session.client('ec2')

    response = ssm_client.describe_instance_information()
    instances = response['InstanceInformationList']
    
    instance_details = []

    for instance in instances:
        instance_id = instance['InstanceId']
        ec2_response = ec2_client.describe_instances(InstanceIds=[instance_id])
        ec2_instance = ec2_response['Reservations'][0]['Instances'][0]
        
        instance_name = 'Unknown'
        for tag in ec2_instance.get('Tags', []):
            if tag['Key'] == 'Name':
                instance_name = tag['Value']
                break
        
        instance_ip = ec2_instance.get('PrivateIpAddress', 'Unknown')

        instance_details.append({
            'InstanceId': instance_id,
            'InstanceName': instance_name,
            'InstanceIP': instance_ip,
            'PlatformName': instance.get('PlatformName', 'Unknown')
        })

    return instance_details

def connect_to_instance(instance_id, profile=None):
    session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    ssm_client = session.client('ssm')

    response = ssm_client.start_session(Target=instance_id)
    session_id = response['SessionId']
    
    # Use AWS CLI to connect to the instance via SSM
    cmd = ['aws', 'ssm', 'start-session', '--target', instance_id]
    if profile:
        cmd.extend(['--profile', profile])
    
    subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description='Connect to AWS SSM instances.')
    parser.add_argument('--profile', type=str, help='AWS CLI profile name', required=False)
    args = parser.parse_args()

    profile = args.profile

    instances = list_ssm_instances(profile)

    if not instances:
        print("No SSM instances found.")
        sys.exit(1)

    print("SSM Instances:")
    for index, instance in enumerate(instances):
        print(f"{index + 1}. {instance['InstanceId']} - {instance['InstanceName']} - {instance['InstanceIP']} - {instance['PlatformName']}")

    selected_index = int(input("Select an instance by number: ")) - 1

    if selected_index < 0 or selected_index >= len(instances):
        print("Invalid selection.")
        sys.exit(1)

    instance_id = instances[selected_index]['InstanceId']
    connect_to_instance(instance_id, profile)

if __name__ == '__main__':
    main()