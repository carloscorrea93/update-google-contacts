import json
import logging
import os

from google.oauth2.credentials import Credentials as GCredentials

from src.flow import flow

CREDENTIALS_FILE = os.path.join(os.getcwd(), 'credentials.json')


class Credentials(object):
    def __init__(self):
        self.flow = flow
        self.CREDENTIALS_FILE = CREDENTIALS_FILE
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def get_credentials(self):
        credentials_dict = self.get_credentials_from_file()
        if credentials_dict:
            credentials = self.generate_credentials_from_dict(credentials_dict)
        else:
            credentials = self.generate_credentials_from_local_server()
        return credentials

    def get_credentials_from_file(self):
        content = None
        try:
            file = open(self.CREDENTIALS_FILE)
            content = json.load(file)
            file.close()
        except Exception as e:
            self.logger.error(e)
        return content

    def generate_credentials_from_local_server(self):
        credentials = self.flow.run_local_server(open_browser=True)
        file = open(self.CREDENTIALS_FILE, 'w+')
        file.write(credentials.to_json())
        file.close()
        return credentials

    @staticmethod
    def generate_credentials_from_dict(credentials_dict):
        return GCredentials(**credentials_dict)
