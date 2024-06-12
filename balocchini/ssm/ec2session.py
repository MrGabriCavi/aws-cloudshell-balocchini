# balocchini/ssm/ec2session.py

import boto3
import subprocess


class EC2Session:
    def __init__(self, session):
        self.ssm = session.client('ssm')
        self.ec2 = session.client('ec2')

    def list_ssm_instances(self):
        """Elenca le istanze EC2 compatibili con SSM."""
        response = self.ssm.describe_instance_information()
        instances = response['InstanceInformationList']

        instance_details = []

        for instance in instances:
            instance_id = instance['InstanceId']
            ec2_response = self.ec2.describe_instances(InstanceIds=[instance_id])
            ec2_instance = ec2_response['Reservations'][0]['Instances'][0]

            instance_name = 'Unknown'
            for tag in ec2_instance.get('Tags', []):
                if tag['Key'] == 'Name':
                    instance_name = tag['Value']
                    break

            instance_ip = ec2_instance.get('PrivateIpAddress', 'Unknown')
            instance_region = ec2_instance['Placement']['AvailabilityZone'][:-1]

            instance_details.append({
                'InstanceId': instance_id,
                'InstanceName': instance_name,
                'InstanceIP': instance_ip,
                'PlatformName': instance.get('PlatformName', 'Unknown'),
                'Region': instance_region
            })

        return instance_details

    def start_session(self, instance_id, region, profile=None):
        """Avvia una sessione SSM con l'istanza specificata."""
        try:
            print(f"Avviamento della sessione SSM con l'istanza {instance_id} nella regione {region}...")
            cmd = ['aws', 'ssm', 'start-session', '--target', instance_id, '--region', region]
            if profile:
                cmd.extend(['--profile', profile])
            subprocess.run(cmd)
        except Exception as e:
            print(f"Errore nell'avvio della sessione SSM: {e}")