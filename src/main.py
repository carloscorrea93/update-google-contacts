import logging

from src.client import PeopleClient
from src.consts import ALL_PERSON_FIELDS
from src.credentials import Credentials
from src.utils import clean_phone_number, should_update_mx_phone_number

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("update_contacts")
logger.setLevel(level=logging.INFO)

credentials = Credentials().get_credentials()
client = PeopleClient(credentials=credentials)
contacts_response = client.contact_group_get(max_members=10)
group_members = contacts_response['memberResourceNames']
logger.info(
    'resourceName: {resource_name}'.format(
        resource_name=contacts_response['resourceName'],
    ),
)
logger.info(
    'memberCount: {member_count}'.format(
        member_count=contacts_response.get('memberCount', 0),
    ),
)
print('\n')
for group_member in group_members:
    contact = client.people_get(
        resource_name=group_member,
        person_fields=[
            ALL_PERSON_FIELDS.get('NAMES'),
            ALL_PERSON_FIELDS.get('PHONE_NUMBERS'),
        ],
    )
    etag = contact['etag']
    names = contact['names']
    phone_numbers = contact['phoneNumbers']
    name = names[0]['displayName'] if names[0] else ''
    logger.info(
        'Name: {name}'.format(
            name=name,
        ),
    )
    should_update = False
    for index, phone_number_object in enumerate(phone_numbers):
        phone_number = clean_phone_number(phone_number_object['value'])
        should_update = should_update_mx_phone_number(phone_number)
        logger.info(
            '#{index} "{type}": {phone_number} -> update: {should_update}'.format(
                index=index+1,
                phone_number=phone_number,
                type=phone_number_object.get('type', ''),
                should_update=should_update,
            ),
        )
    print('\n')
