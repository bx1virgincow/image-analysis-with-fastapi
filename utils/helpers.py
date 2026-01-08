import os
from email.header import Header

from fastapi import UploadFile, HTTPException
import logging

#simple logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger("image_api")

#local storage
IMAGE_DIRECTORY = os.path.join(os.getcwd(), "data", "images")
os.makedirs(IMAGE_DIRECTORY, exist_ok=True)

ALLOWED_TYPES = {"image/jpeg", "image/png"}

#validate image
def validate_image(file: UploadFile):
    content_type = file.content_type.strip().lower()
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400,detail="Unsupported image type")
    if not file.filename:
        raise HTTPException(status_code=400,detail="Missing filename")

#an extension to check file type
def allowed_file_type(file_type: str)->str:
    if file_type == "image/jpeg":
        return ".jpg"
    if file_type == "image/png":
        return ".png"
    raise HTTPException(status_code=400,detail="Unsupported file type")

#auth key
API_KEY = os.getenv("API_KEY")

#verify the key
async def verify_api_key(x_api_key: str = Header(None)):
    if not API_KEY: # If no API_KEY set, skip auth (dev mode)
        return
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
