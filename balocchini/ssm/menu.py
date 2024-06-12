# balocchini/ssm/menu.py

from .ec2session import EC2Session
from .operation import SSMOperation

class SSMMenu:
    def __init__(self, session):
        self.ec2_session = EC2Session(session)
        self.ssm_operation = SSMOperation(self.ec2_session)

    def display_menu(self, instance_id=None):
        if instance_id:
            instances = self.ec2_session.list_ssm_instances()
            instance = next((inst for inst in instances if inst['InstanceId'] == instance_id), None)
            if instance:
                self.ssm_operation.display_operations(instance_id, instance['Region'])
            else:
                print(f"Istanza {instance_id} non trovata.")
            return

        while True:
            print("\nOperazioni SSM:")
            print("1. start-session")
            print("q. torna-al-menu-principale")
            choice = input("Inserisci il numero o il nome dell'operazione: ").strip().lower()

            if choice in ['1', 'start-session']:
                instances = self.ec2_session.list_ssm_instances()
                if not instances:
                    print("Nessuna istanza compatibile con SSM trovata.")
                    return

                print("\nIstanze EC2 compatibili con SSM:")
                for i, instance in enumerate(instances):
                    print(f"{i + 1}. {instance['InstanceId']} - {instance['InstanceName']} - {instance['InstanceIP']} - {instance['PlatformName']}")

                choice = input("Inserisci il numero dell'istanza per avviare la sessione SSM: ").strip()
                try:
                    instance = instances[int(choice) - 1]
                    self.ssm_operation.display_operations(instance['InstanceId'], instance['Region'])
                    break
                except (IndexError, ValueError):
                    print("Scelta non valida. Riprova.")
            elif choice == 'q':
                break
            else:
                print("Scelta non valida. Riprova.")