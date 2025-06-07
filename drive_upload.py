import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import streamlit as st

def upload_to_drive(file, mimetype=None):
    """
    Upload a file-like object to Google Drive and return the shareable link.

    Args:
        file: file-like object with `.read()` and optionally `.name` and `.type`
        mimetype: str, optional MIME type if file.type is missing

    Returns:
        str: shareable Google Drive link
    """
    # Load service account info from Streamlit secrets (already parsed dict)
    service_account_info = st.secrets["gcp_service_account"]

    creds = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )

    drive_service = build("drive", "v3", credentials=creds)

    # Use file.name or fallback
    filename = getattr(file, "name", "uploaded_file")

    file_metadata = {
        "name": filename,
        # "parents": ["YOUR_FOLDER_ID_HERE"]  # Uncomment and set if needed
    }

    # Determine mime type: use file.type if available else mimetype param else default
    actual_mimetype = getattr(file, "type", None) or mimetype or "application/octet-stream"

    # Reset file pointer before reading
    file.seek(0)

    # Read file bytes into BytesIO
    file_bytes = io.BytesIO(file.read())

    # Reset pointer again to start for upload
    file_bytes.seek(0)

    media = MediaIoBaseUpload(file_bytes, mimetype=actual_mimetype)

    uploaded = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    file_id = uploaded.get("id")

    # Make the file public readable
    drive_service.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"},
    ).execute()

    # Return view link
    return f"https://drive.google.com/file/d/{file_id}/view"
