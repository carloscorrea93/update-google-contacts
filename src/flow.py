import os

from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = os.path.join(os.getcwd(), 'client_secrets.json')
SCOPES = [
    'https://www.googleapis.com/auth/contacts',
    'https://www.googleapis.com/auth/contacts.other.readonly',
    'https://www.googleapis.com/auth/contacts.readonly',
    'https://www.googleapis.com/auth/directory.readonly',
    'https://www.googleapis.com/auth/user.addresses.read',
    'https://www.googleapis.com/auth/user.birthday.read',
    'https://www.googleapis.com/auth/user.emails.read',
    'https://www.googleapis.com/auth/user.gender.read',
    'https://www.googleapis.com/auth/user.organization.read',
    'https://www.googleapis.com/auth/user.phonenumbers.read',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]
flow = InstalledAppFlow.from_client_secrets_file(
    client_secrets_file=CLIENT_SECRETS_FILE, scopes=SCOPES,
)
