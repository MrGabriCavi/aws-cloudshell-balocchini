# balocchini/sts/menu.py

from .operation import STSOperation

class STSMenu:
    def __init__(self, session):
        self.sts_operation = STSOperation(session)

    def display_menu(self, role_arn=None, role_session_name=None, target_profile=None):
        if not role_arn:
            role_arn = input("Inserisci l'ARN del ruolo da assumere: ").strip()

        if not role_session_name:
            role_session_name = input("Inserisci il nome della sessione per il ruolo da assumere: ").strip()

        if not target_profile:
            target_profile = input("Inserisci il nome del profilo target da aggiornare: ").strip()

        credentials = self.sts_operation.assume_role(role_arn, role_session_name)
        self.sts_operation.update_profile(target_profile, credentials)