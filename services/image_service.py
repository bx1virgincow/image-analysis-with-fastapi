import os
import uuid
from fastapi import UploadFile,HTTPException
from utils.helpers import validate_image, IMAGE_DIRECTORY, allowed_file_type

#implementation of the service itself
def analyze_image(image_id: str):
    # here we check for file extension
    paths = [
        os.path.join(IMAGE_DIRECTORY, f"{image_id}.jpg"),
        os.path.join(IMAGE_DIRECTORY, f"{image_id}.png"),
    ]

    image_path = next((p for p in paths if os.path.exists(p)), None)
    if not image_path:
        raise HTTPException(status_code=404, detail="Image not found")

    #mocking the analysis
    mock_results = {
        "image_id": image_id,
        "image_path": "Oily",
        "issue": ["Hyperpigmentation", "Enlarged pores"],
        "confidence": 0.07
    }

    return mock_results

#save results to local storage
async def save_image(file: UploadFile):
    validate_image(file)

    #read content
    content = await file.read()
    #convert to 5mb
    max_bytes = 5 * 1024 * 1024

    if len(content) > max_bytes:
        raise HTTPException(status_code=400, detail="file too large")
    image_id = str(uuid.uuid4())
    ext = allowed_file_type(file.content_type)
    print(f"image_id: {image_id}")
    save_path = os.path.join(IMAGE_DIRECTORY, f"{image_id}.{ext}")

    #write file safely
    with open(save_path, "wb") as f:
        f.write(content)

    return {"image_id": image_id}
