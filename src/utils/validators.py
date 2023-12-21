from fastapi import HTTPException
import requests

allowed_file_types = [
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/pdf",
    "text/plain",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
]


def file_upload_validator(files):
    for file in files:
        if file.content_type not in allowed_file_types:
            raise HTTPException(
                status_code=400,
                detail="Your file must be in (pdf, txt, md, dock, pptx, cvs) format and less than 15 MB!",
            )
    return files



def notion_validator(obj):
    headers = {
        "Authorization": "Bearer " + obj.token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    res = requests.post(
        url=f"https://api.notion.com/v1/databases/{obj.database_id}/query",
        headers=headers,
    )
    print(res)
    if res.status_code == 200:
        return obj
    else:
        raise HTTPException(status_code=404, detail=f"{obj.title} not found!")