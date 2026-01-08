from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from pydantic import BaseModel
from utils.helpers import verify_api_key
from services.image_service import save_image, analyze_image

router = APIRouter(tags=["Image"])

class AnalyzeImageResults(BaseModel):
    image_id: str

@router.post("/upload")
async def upload_image(file: UploadFile = File(...),
                       api_key: None = Depends(verify_api_key)):
    try:
        result = await save_image(file)
        return result
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error")

@router.post("/debug-upload")
async def debug_upload(file: UploadFile = File(...)):
    return {"filename": file.filename, "content_type": file.content_type}



@router.post("/analyze")
def analyze(payload: AnalyzeImageResults,
                  api_key: None = Depends(verify_api_key)):
    try:
        return analyze_image(payload.image_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error")
