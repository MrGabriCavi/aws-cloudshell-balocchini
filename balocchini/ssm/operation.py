# balocchini/ssm/operation.py

class SSMOperation:
    def __init__(self, ec2_session):
        self.ec2_session = ec2_session

    def display_operations(self, instance_id, region):
        while True:
            print("\nOperazioni SSM:")
            print("1. start-session")
            print("q. torna-al-menu-principale")
            choice = input("Inserisci il numero o il nome dell'operazione: ").strip().lower()

            if choice in ['1', 'start-session']:
                self.ec2_session.start_session(instance_id, region)
            elif choice == 'q':
                break
            else:
                print("Scelta non valida. Riprova.")