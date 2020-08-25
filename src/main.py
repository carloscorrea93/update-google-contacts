import argparse
import logging
import time

from src.client import PeopleClient
from src.consts import ALL_PERSON_FIELDS
from src.credentials import Credentials
from src.utils import (
    clean_mx_with_regex,
    clean_phone_number,
    should_update_mx_phone_number,
)

logging.basicConfig(level=logging.INFO)


class RunScript(object):
    def __init__(self):
        credentials = Credentials().get_credentials()
        self.logger = logging.getLogger('update_contacts')
        self.logger.setLevel(level=logging.INFO)
        self.client = PeopleClient(credentials=credentials)

    def main(self):
        enable_delete = self.parse_arguments()
        contacts_response = self.client.contact_group_get(max_members=200)
        group_members = contacts_response['memberResourceNames']
        self.logger.info(
            'resourceName: {resource_name}'.format(
                resource_name=contacts_response['resourceName'],
            ),
        )
        self.logger.info(
            'memberCount: {member_count}'.format(
                member_count=contacts_response.get('memberCount', 0),
            ),
        )
        print('\n')
        offset = 0
        for index, resource_name in enumerate(group_members[offset]):
            time.sleep(2)
            contact = self.get_people(resource_name)
            etag, phone_numbers, name = self.parse_contact(contact)
            self.logger.info(
                '#index:{index} Name: {name}'.format(
                    index=index + offset + 1,
                    name=name,
                ),
            )
            delete_contact = False
            if enable_delete:
                if self.delete_contact_question(name):
                    delete_contact = True
                    self.process_delete(resource_name)
            if not delete_contact:
                should_update = self.process_phones(phone_numbers)
                if should_update:
                    if self.process_contact_question(name):
                        self.process_update(
                            contact,
                            resource_name,
                            phone_numbers,
                        )
            print('\n')

    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--enable-delete',
            help='enable delete option',
            action='store_true',
        )
        args = parser.parse_args()
        enable_delete = args.enable_delete
        return enable_delete

    def get_people(self, resource_name):
        return self.client.people_get(
            resource_name=resource_name,
            person_fields=[
                ALL_PERSON_FIELDS.get('NAMES'),
                ALL_PERSON_FIELDS.get('PHONE_NUMBERS'),
            ],
        )

    def parse_contact(self, contact):
        etag = contact['etag']
        names = contact['names']
        phone_numbers = contact.get('phoneNumbers', [])
        name = names[0]['displayName'] if names[0] else ''
        return etag, phone_numbers, name

    def process_phones(self, phone_numbers):
        should_update = False
        for index, phone_number_object in enumerate(phone_numbers):
            phone_number = clean_phone_number(phone_number_object['value'])
            should_update = should_update_mx_phone_number(phone_number)
            if should_update:
                should_update = True
            self.logger.info(
                '#{index} "{type}": {phone_number}'.format(
                    index=index + 1,
                    phone_number=phone_number,
                    type=phone_number_object.get('type', ''),
                ),
            )
        return should_update

    def process_delete(self, resource_name):
        self.client.people_delete(resource_name)

    def delete_contact_question(self, name):
        check = str(
            input("Delete this contact '{name}' ? (Y/N): ".format(name=name)),
        ).lower().strip()
        try:
            if check[0] == 'y':
                return True
            elif check[0] == 'n':
                return False
            else:
                return self.delete_contact_question(name)
        except Exception as e:
            self.logger.error(e)
            return self.delete_contact_question(name)

    def process_contact_question(self, name):
        check = str(
            input(
                "Update this contact number '{name}' ? (Y/N): ".format(
                    name=name,
                ),
            ),
        ).lower().strip()
        try:
            if check[0] == 'y':
                return True
            elif check[0] == 'n':
                return False
            else:
                return self.process_contact_question(name)
        except Exception as e:
            self.logger.error(e)
            return self.process_contact_question(name)

    def process_update(self, contact, resource_name, phone_numbers):
        body = self.create_update_body(contact)
        body['phoneNumbers'] = self.update_phone_numbers(phone_numbers)
        self.client.people_update(
            resource_name,
            body,
            person_fields=[
                ALL_PERSON_FIELDS.get('PHONE_NUMBERS'),
            ],
        )

    def create_update_body(self, body):
        body.pop('resourceName')
        body.pop('names')
        return body

    def update_phone_numbers(self, phone_numbers):
        for phone_number_object in phone_numbers:
            phone_number = clean_phone_number(phone_number_object['value'])
            if should_update_mx_phone_number(phone_number):
                phone_number_object['value'] = clean_mx_with_regex(
                    phone_number,
                )
        return phone_numbers


if __name__ == '__main__':
    RunScript().main()
