import os
from google_auth_oauthlib.flow import Flow
from django.conf import settings

def get_google_flow():
    flow = Flow.from_client_secrets_file(
        os.path.join(settings.BASE_DIR, 'config', 'credentials.json'),
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri='http://127.0.0.1:8000/accounts/google/callback/'
    )
    return flow
