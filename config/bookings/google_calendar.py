from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def create_calendar_event(user, title, start_time, end_time, description):
    # If user has not connected Google Calendar, do nothing
    if not user.google_access_token:
        return

    creds = Credentials(
        token=user.google_access_token,
        refresh_token=user.google_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=None,
        client_secret=None,
        scopes=["https://www.googleapis.com/auth/calendar"]
    )

    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": title,
        "description": description,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "UTC",
        },
    }

    service.events().insert(
        calendarId="primary",
        body=event
    ).execute()
