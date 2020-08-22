import logging

from googleapiclient.discovery import build

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

    def get_all_contact_group(self, resource_name='contactGroups/all', max_members=200):
        return self._execute(
            self.client.contactGroups().get(resourceName=resource_name, maxMembers=max_members),
        )

    def _execute(self, request):
        try:
            return request.execute()
        except Exception as e:
            self.logger.error(e)
