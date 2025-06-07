import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

def upload_to_drive(uploaded_file):
    creds =service_account.Credentials.from_service_account_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/drive.file"]

    )
    service =build('drive','v3',credentials=creds)
    media =MediaIoBaseUpload(uploaded_file,mimetype="application/pdf")
    file_metadata={
        'name': uploaded_file.name

    }
    file=service.files().create(body=file_metadata,media_body=media,fields='id').execute()
    # making files public so that anyone can view 
    service.permissions().create(
        fileId=file.get('id'),
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()
    return f"https://drive.google.com/file/d/{file.get('id')}/view"