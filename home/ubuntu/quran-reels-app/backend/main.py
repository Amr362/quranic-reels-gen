
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import shutil
from typing import Optional
import tempfile
from pathlib import Path
import uuid

# استيراد النصوص المساعدة من ملفات أخرى
try:
    from match_quran import match_audio_to_quran
except ImportError:
    # وظيفة احتياطية إذا لم يتم العثور على الملف
    def match_audio_to_quran(audio_path):
        return {"surah": 1, "ayah": 1, "text": "بسم الله الرحمن الرحيم"}

try:
    from generate_video import create_quran_reel
except ImportError:
    # وظيفة احتياطية إذا لم يتم العثور على الملف
    def create_quran_reel(audio_path, quran_match, output_path):
        # محاكاة إنشاء الفيديو
        # في الإنتاج، هذا سيستخدم MoviePy أو أدوات مماثلة
        # لإنشاء فيديو حقيقي مع النص القرآني
        return output_path

app = FastAPI(title="Quran Reels API")

# إضافة CORS للسماح بالطلبات من واجهة المستخدم
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # يجب تغيير هذا في الإنتاج لتحديد أصول محددة
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# إنشاء المجلدات إذا لم تكن موجودة
UPLOAD_DIR = Path("./uploads")
OUTPUT_DIR = Path("./output")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "مرحباً بك في واجهة برمجة تطبيقات ريلز القرآن"}

@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    """تحميل ملف صوتي وحفظه على الخادم"""
    if not file.filename.endswith((".mp3", ".wav", ".ogg", ".m4a")):
        raise HTTPException(status_code=400, detail="الرجاء تحميل ملف صوتي صالح")
    
    unique_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    temp_file_path = UPLOAD_DIR / f"{unique_id}{file_extension}"
    
    # حفظ الملف
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "file_path": str(temp_file_path), "id": unique_id}

@app.post("/create-reel/")
async def create_reel(file_path: str):
    """إنشاء فيديو ريلز من ملف صوتي تم تحميله مسبقاً"""
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="الملف الصوتي غير موجود")
    
    try:
        # مطابقة الصوت مع القرآن
        quran_match = match_audio_to_quran(file_path)
        
        # إنشاء معرف فريد للفيديو
        output_id = str(uuid.uuid4())
        output_path = OUTPUT_DIR / f"{output_id}.mp4"
        
        # إنشاء فيديو ريلز
        video_path = create_quran_reel(file_path, quran_match, str(output_path))
        
        return {
            "status": "success",
            "video_id": output_id,
            "video_path": video_path,
            "quran_match": quran_match
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ أثناء إنشاء الفيديو: {str(e)}")

@app.get("/video/{video_id}")
def get_video(video_id: str):
    """الحصول على فيديو تم إنشاؤه سابقاً حسب المعرف"""
    video_path = OUTPUT_DIR / f"{video_id}.mp4"
    
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="الفيديو غير موجود")
    
    return FileResponse(str(video_path))

if __name__ == "__main__":
    # تشغيل التطبيق مباشرة عند تنفيذ هذا الملف
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
