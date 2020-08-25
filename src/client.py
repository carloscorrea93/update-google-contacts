import logging

from googleapiclient.discovery import build

from src.consts import ALL_PERSON_FIELDS

API_SERVICE_NAME = 'people'
API_VERSION = 'v1'


class PeopleClient(object):
    def __init__(self, credentials):
        self.client = build(
            API_SERVICE_NAME, API_VERSION,
            credentials=credentials,
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def contact_group_get(self, resource_name='contactGroups/all', max_members=100):
        return self._execute(
            self.client.contactGroups().get(
                resourceName=resource_name,
                maxMembers=max_members,
            ),
        )

    def people_get(self, resource_name, person_fields=None):
        if not person_fields:
            person_fields = list(ALL_PERSON_FIELDS.values())
        return self._execute(
            self.client.people().get(
                resourceName=resource_name,
                personFields=','.join(person_fields),
            ),
        )

    def people_delete(self, resource_name):
        return self._execute(
            self.client.people().deleteContact(
                resourceName=resource_name,
            ),
        )

    def people_update(self, resource_name, body, person_fields=None):
        if not person_fields:
            person_fields = list(ALL_PERSON_FIELDS.values())
        return self._execute(
            self.client.people().updateContact(
                resourceName=resource_name,
                body=body,
                updatePersonFields=','.join(person_fields),
            ),
        )

    def _execute(self, request):
        try:
            return request.execute()
        except Exception as e:
            self.logger.error(e)
