import logging
from unittest.mock import Mock

from expects import be_an, expect, have_keys
from mamba import before, describe, description, it

from spec.fake_response import CONTACT_GROUP_GET
from src.client import PeopleClient

logging.basicConfig(level=logging.INFO)

with description(PeopleClient) as self:
    with before.all:
        self.client = PeopleClient(credentials=Mock())

    with describe(self.client.contact_group_get):
        with it('Get all Contact group'):
            self.client.contact_group_get = Mock(
                return_value=CONTACT_GROUP_GET,
            )
            contacts = self.client.contact_group_get()
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
