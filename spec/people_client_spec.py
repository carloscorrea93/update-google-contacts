import logging
from unittest.mock import Mock

from expects import be_an, expect, have_keys
from mamba import before, describe, description, it

from spec.fake_response import GET_ALL_CONTACTS_GROUP_RESPONSE
from src.client import PeopleClient

logging.basicConfig(level=logging.INFO)

with description(PeopleClient) as self:
    with before.all:
        self.client = PeopleClient(credentials=Mock())

    with describe(self.client.get_all_contact_group):
        with it('Get all Contact group'):
            self.client.get_all_contact_group = Mock(
                return_value=GET_ALL_CONTACTS_GROUP_RESPONSE,
            )
            contacts = self.client.get_all_contact_group()
            expect(contacts).to(
                have_keys(
                    'resourceName',
                    'groupType',
                    'name',
                    'formattedName',
                    'memberResourceNames',
                    'memberCount',
                ),
            )
            expect(contacts['memberResourceNames']).to(be_an(list))
            expect(contacts['memberCount']).to(be_an(int))
