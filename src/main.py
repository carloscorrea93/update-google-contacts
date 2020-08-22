import logging

from src.client import PeopleClient
from src.credentials import Credentials

logging.basicConfig(level=logging.INFO)


def main():
    credentials = Credentials().get_credentials()
    client = PeopleClient(credentials=credentials)
    contacts_response = client.get_all_contact_group()
    logging.info(
        'resourceName: {resource_name}'.format(
            resource_name=contacts_response['resourceName'],
        ),
    )
    logging.info(
        'memberCount: {member_count}'.format(
            member_count=contacts_response['memberCount'],
        ),
    )


if __name__ == '__main__':
    main()
