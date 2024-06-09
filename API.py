# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 00:42:10 2023

@author: Jaka
"""
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scopes required for accessing the Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def retrieve_messages_from_sender(service, sender_email):
    messages = []
    page_token = None

    while True:
        # Define a query to filter messages by sender's email
        query = f"from:{sender_email}"

        # Get a page of messages matching the query
        response = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
        messages.extend(response.get('messages', []))

        # Check if there are more pages
        page_token = response.get('nextPageToken')
        if not page_token:
            break

    return messages

if __name__ == "__main__":
    # Load the client secrets file and build the Gmail service as before
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    credentials = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=credentials)

    # Define the sender's Gmail address
    sender_email = "noreply-maps-issues@google.com"  # Replace with the desired sender's email address

    # Retrieve all messages from the specified sender
    sender_messages = retrieve_messages_from_sender(service, sender_email)

    # Print all messages from the sender and count them
    print(f"Messages from {sender_email}:\n")
    message_count = 0

    for message_info in sender_messages:
        message_id = message_info['id']
        msg = service.users().messages().get(userId='me', id=message_id).execute()
        
        # Retrieve the subject from the message's headers
        subject = None
        for header in msg['payload']['headers']:
            if header['name'] == 'Subject':
                subject = header['value']
                break
        
        print(f"Subject: {subject}")
        print(f"Date: {msg['internalDate']}")
        print("------")
        message_count += 1

    print(f"\nTotal messages from {sender_email}: {message_count}")
