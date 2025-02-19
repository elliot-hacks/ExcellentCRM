import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "/credentials.json"  # Update this path

def get_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("calendar", "v3", credentials=credentials)

def create_google_calendar_event(event):
    service = get_calendar_service()
    calendar_id = "primary"

    event_data = {
        "summary": event.title,
        "description": event.description,
        "start": {"dateTime": event.start_time.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": event.end_time.isoformat(), "timeZone": "UTC"},
        "conferenceData": {
            "createRequest": {"requestId": f"meeting-{event.id}"}
        },
    }

    created_event = service.events().insert(
        calendarId=calendar_id,
        body=event_data,
        conferenceDataVersion=1
    ).execute()

    event.meeting_link = created_event["hangoutLink"]
    event.calendar_event_id = created_event["id"]
    event.save()
    return event.meeting_link
