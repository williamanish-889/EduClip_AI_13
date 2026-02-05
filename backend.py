"""
EduClip AI - Enhanced Backend
Supports: YouTube URL + Direct Upload
Deployment: Render.com ready
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
import os
import uuid
import shutil
import json
from datetime import datetime, timedelta
import asyncio
from pathlib import Path
import logging

# JWT and Security
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import hashlib

# Initialize FastAPI
app = FastAPI(
    title="EduClip AI API",
    description="AI-Enhanced Video Processing Platform",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

# Storage directories
UPLOAD_DIR = Path("storage/uploads")
CLIPS_DIR = Path("storage/clips")
THUMBNAILS_DIR = Path("storage/thumbnails")

# Create directories
for directory in [UPLOAD_DIR, CLIPS_DIR, THUMBNAILS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Security functions
def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return hash_password(plain_password) == hashed_password

security = HTTPBearer()

# JWT token creation
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# In-memory database (replace with PostgreSQL in production)
users_db = {}
videos_db = {}
transcripts_db = {}
summaries_db = {}
clips_db = {}
analytics_db = {}

# Pydantic Models
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "student"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class VideoURLInput(BaseModel):
    url: HttpUrl
    title: str
    description: Optional[str] = None

class VideoProcessingStatus(BaseModel):
    video_id: str
    status: str
    progress: int
    message: str

# Pydantic Models
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        user = users_db.get(email)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# YouTube Download Function (using yt-dlp)
async def download_youtube_video(url: str, output_path: Path) -> dict:
    """Download video from YouTube URL"""
    try:
        # Import yt-dlp
        import yt_dlp
        
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': str(output_path / '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            return {
                'success': True,
                'filename': filename,
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
            }
    except Exception as e:
        logger.error(f"YouTube download error: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

# Simulated AI Processing Functions
async def process_video_ai(video_id: str):
    """Simulate AI processing pipeline"""
    try:
        video = videos_db[video_id]
        
        # Update status: Transcribing
        video['status'] = 'transcribing'
        video['progress'] = 20
        await asyncio.sleep(2)
        
        # Simulate transcript generation
        transcript = {
            'transcript_id': str(uuid.uuid4()),
            'video_id': video_id,
            'full_text': 'This is a simulated transcript of the video content. In production, this would be generated by Whisper AI.',
            'segments': [
                {'start': 0.0, 'end': 5.0, 'text': 'Introduction to the topic'},
                {'start': 5.0, 'end': 15.0, 'text': 'Main concept explanation'},
                {'start': 15.0, 'end': 25.0, 'text': 'Detailed examples and use cases'},
                {'start': 25.0, 'end': 30.0, 'text': 'Conclusion and summary'},
            ],
            'language': 'en',
            'confidence_score': 0.95,
            'created_at': datetime.utcnow().isoformat()
        }
        transcripts_db[video_id] = transcript
        
        # Update status: Analyzing
        video['status'] = 'analyzing'
        video['progress'] = 50
        await asyncio.sleep(2)
        
        # Simulate summary generation
        summary = {
            'summary_id': str(uuid.uuid4()),
            'video_id': video_id,
            'executive_summary': 'This video covers fundamental concepts with practical examples. Perfect for beginners and intermediate learners.',
            'key_concepts': [
                'Fundamental principles',
                'Practical applications',
                'Best practices',
                'Common pitfalls to avoid'
            ],
            'learning_objectives': [
                'Understand core concepts',
                'Apply knowledge practically',
                'Develop problem-solving skills'
            ],
            'topics': [
                {'name': 'Introduction', 'timestamp': 0.0},
                {'name': 'Main Content', 'timestamp': 5.0},
                {'name': 'Examples', 'timestamp': 15.0},
                {'name': 'Conclusion', 'timestamp': 25.0}
            ],
            'difficulty_level': 'intermediate',
            'key_takeaways': [
                'Core concept mastery is essential',
                'Practice with real examples',
                'Continuous learning is key'
            ],
            'created_at': datetime.utcnow().isoformat()
        }
        summaries_db[video_id] = summary
        
        # Update status: Generating clips
        video['status'] = 'generating_clips'
        video['progress'] = 80
        await asyncio.sleep(2)
        
        # Simulate clip generation
        clip_ids = []
        for i, topic in enumerate(summary['topics']):
            clip_id = str(uuid.uuid4())
            clip = {
                'clip_id': clip_id,
                'video_id': video_id,
                'title': topic['name'],
                'description': f'Focused clip on {topic["name"]}',
                'start_time': topic['timestamp'],
                'end_time': topic['timestamp'] + 10.0,
                'duration': 10.0,
                'importance_score': 0.8 - (i * 0.1),
                'file_path': f'clips/clip_{clip_id}.mp4',
                'thumbnail_path': f'thumbnails/thumb_{clip_id}.jpg',
                'views': 0,
                'created_at': datetime.utcnow().isoformat()
            }
            clips_db[clip_id] = clip
            clip_ids.append(clip_id)
        
        # Update status: Complete
        video['status'] = 'complete'
        video['progress'] = 100
        video['processed_at'] = datetime.utcnow().isoformat()
        video['clip_ids'] = clip_ids
        
        logger.info(f"Video {video_id} processed successfully")
        
    except Exception as e:
        logger.error(f"Processing error for video {video_id}: {str(e)}")
        video['status'] = 'failed'
        video['progress'] = 0

# API Endpoints

@app.get("/")
async def root():
    return {
        "message": "EduClip AI API v2.0",
        "status": "online",
        "features": ["YouTube URL", "Direct Upload", "AI Processing"],
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0"
    }

@app.post("/api/auth/register", response_model=Token)
async def register(user: UserRegister):
    """Register a new user"""
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = str(uuid.uuid4())
    hashed_password = hash_password(user.password)
    
    user_data = {
        "user_id": user_id,
        "username": user.username,
        "email": user.email,
        "password_hash": hashed_password,
        "role": user.role,
        "created_at": datetime.utcnow().isoformat(),
        "is_active": True
    }
    
    users_db[user.email] = user_data
    
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }

@app.post("/api/auth/login", response_model=Token)
async def login(user: UserLogin):
    """Login user"""
    user_data = users_db.get(user.email)
    
    if not user_data or not verify_password(user.password, user_data["password_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user_data["user_id"],
            "username": user_data["username"],
            "email": user_data["email"],
            "role": user_data["role"]
        }
    }

@app.post("/api/videos/upload")
async def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    """Upload video directly"""
    try:
        # Validate file type
        allowed_types = ['video/mp4', 'video/avi', 'video/mov', 'video/mkv', 'video/webm']
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type. Supported: MP4, AVI, MOV, MKV, WEBM")
        
        # Generate video ID
        video_id = str(uuid.uuid4())
        
        # Save file
        file_path = UPLOAD_DIR / f"{video_id}_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create video record
        video_data = {
            "video_id": video_id,
            "user_id": current_user["user_id"],
            "title": title,
            "description": description,
            "file_path": str(file_path),
            "filename": file.filename,
            "status": "processing",
            "progress": 0,
            "uploaded_at": datetime.utcnow().isoformat(),
            "views": 0,
            "source": "upload"
        }
        
        videos_db[video_id] = video_data
        
        # Start background processing
        background_tasks.add_task(process_video_ai, video_id)
        
        return {
            "success": True,
            "video_id": video_id,
            "message": "Video uploaded successfully. Processing started.",
            "status": "processing"
        }
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/api/videos/youtube")
async def process_youtube_url(
    background_tasks: BackgroundTasks,
    data: VideoURLInput,
    current_user: dict = Depends(get_current_user)
):
    """Process video from YouTube URL"""
    try:
        video_id = str(uuid.uuid4())
        
        # Create initial video record
        video_data = {
            "video_id": video_id,
            "user_id": current_user["user_id"],
            "title": data.title,
            "description": data.description,
            "url": str(data.url),
            "status": "downloading",
            "progress": 0,
            "uploaded_at": datetime.utcnow().isoformat(),
            "views": 0,
            "source": "youtube"
        }
        
        videos_db[video_id] = video_data
        
        # Download and process in background
        async def download_and_process():
            # Download video
            result = await download_youtube_video(str(data.url), UPLOAD_DIR)
            
            if result['success']:
                video_data['file_path'] = result['filename']
                video_data['status'] = 'processing'
                video_data['progress'] = 10
                
                # Start AI processing
                await process_video_ai(video_id)
            else:
                video_data['status'] = 'failed'
                video_data['error'] = result.get('error', 'Download failed')
        
        background_tasks.add_task(download_and_process)
        
        return {
            "success": True,
            "video_id": video_id,
            "message": "YouTube video download started. Processing will begin automatically.",
            "status": "downloading"
        }
        
    except Exception as e:
        logger.error(f"YouTube processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/api/videos/{video_id}/status")
async def get_video_status(
    video_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get video processing status"""
    video = videos_db.get(video_id)
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return {
        "video_id": video_id,
        "status": video["status"],
        "progress": video["progress"],
        "title": video["title"],
        "source": video.get("source", "upload")
    }

@app.get("/api/videos/{video_id}/transcript")
async def get_transcript(
    video_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get video transcript"""
    transcript = transcripts_db.get(video_id)
    
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    
    return transcript

@app.get("/api/videos/{video_id}/summary")
async def get_summary(
    video_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get video summary"""
    summary = summaries_db.get(video_id)
    
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    
    return summary

@app.get("/api/videos/{video_id}/clips")
async def get_clips(
    video_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get video clips"""
    video = videos_db.get(video_id)
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    clip_ids = video.get('clip_ids', [])
    clips = [clips_db[clip_id] for clip_id in clip_ids if clip_id in clips_db]
    
    return {"clips": clips, "total": len(clips)}

@app.get("/api/videos")
async def list_videos(
    current_user: dict = Depends(get_current_user)
):
    """List all videos for current user"""
    user_videos = [
        {
            "video_id": v["video_id"],
            "title": v["title"],
            "description": v.get("description"),
            "status": v["status"],
            "progress": v["progress"],
            "uploaded_at": v["uploaded_at"],
            "source": v.get("source", "upload"),
            "views": v.get("views", 0)
        }
        for v in videos_db.values()
        if v["user_id"] == current_user["user_id"]
    ]
    
    return {"videos": user_videos, "total": len(user_videos)}

@app.get("/api/analytics/dashboard")
async def get_dashboard(
    current_user: dict = Depends(get_current_user)
):
    """Get analytics dashboard data"""
    user_videos = [v for v in videos_db.values() if v["user_id"] == current_user["user_id"]]
    
    total_videos = len(user_videos)
    completed_videos = len([v for v in user_videos if v["status"] == "complete"])
    total_clips = sum(len(v.get("clip_ids", [])) for v in user_videos)
    total_views = sum(v.get("views", 0) for v in user_videos)
    
    return {
        "total_videos": total_videos,
        "completed_videos": completed_videos,
        "processing_videos": total_videos - completed_videos,
        "total_clips": total_clips,
        "total_views": total_views,
        "recent_videos": user_videos[:5]
    }

@app.delete("/api/videos/{video_id}")
async def delete_video(
    video_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a video"""
    video = videos_db.get(video_id)
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    if video["user_id"] != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Delete files
    if "file_path" in video:
        file_path = Path(video["file_path"])
        if file_path.exists():
            file_path.unlink()
    
    # Delete from databases
    videos_db.pop(video_id, None)
    transcripts_db.pop(video_id, None)
    summaries_db.pop(video_id, None)
    
    # Delete clips
    clip_ids = video.get("clip_ids", [])
    for clip_id in clip_ids:
        clips_db.pop(clip_id, None)
    
    return {"success": True, "message": "Video deleted successfully"}

# Run server
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
