# 🎓 EduClip AI v2.0

> Transform educational videos with AI - Dual input modes, modern 3D UI, instant deployment

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ What's New in v2.0

### 🎥 Dual Input Modes
- **Direct Upload**: Drag & drop your video files (MP4, AVI, MOV, MKV, WEBM)
- **YouTube URL**: Process any public YouTube video instantly

### 🎨 Modern 3D UI
- Glassmorphism design with animated gradients
- Smooth transitions and micro-interactions
- Responsive mobile-first approach
- Dark theme with beautiful color schemes

### 🚀 Production Ready
- One-click deployment to Render
- Zero configuration required
- Automatic scaling and SSL
- Enterprise-grade security

---

## 🌟 Features

### For Educators
- 📤 Upload or link course videos
- 🎤 Automatic speech-to-text transcription
- 📝 AI-powered content summarization
- ✂️ Smart highlight detection and clip generation
- 📊 Analytics dashboard for engagement tracking
- 🔗 Easy sharing on social media and LMS

### For Students
- 🔍 Searchable video library
- ⚡ Quick access to key concepts
- 📖 Read summaries before watching
- 🎯 Focus on important segments
- 📈 Track learning progress

### Technical Excellence
- 🤖 AI/ML Integration (Whisper, Gemini)
- 🔐 JWT Authentication & Security
- 💾 Efficient data management
- 🌐 RESTful API design
- 📱 Mobile responsive interface
- ⚡ Real-time processing updates

---

## 🚀 Quick Start

### Option 1: Deploy to Render (Recommended)

1. **Click "Deploy to Render" button above**
2. **Connect your GitHub account**
3. **Set environment variables:**
   - `SECRET_KEY`: Generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"`
   - `GEMINI_API_KEY`: (Optional) Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
4. **Click "Create Web Service"**
5. **Done!** Your app is live in 3 minutes

### Option 2: Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/educlip-ai-v2.git
cd educlip-ai-v2

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SECRET_KEY="your-secret-key"
export GEMINI_API_KEY="your-api-key"  # Optional

# Run backend
python backend.py

# Open frontend
# Simply open index.html in browser or:
python -m http.server 8080
```

Access the app:
- Frontend: `http://localhost:8080`
- API Docs: `http://localhost:8000/docs`

---

## 📸 Screenshots

### Modern Dashboard
![Dashboard](https://via.placeholder.com/800x450/667eea/ffffff?text=Beautiful+3D+Dashboard)

### Dual Upload Modes
![Upload](https://via.placeholder.com/800x450/764ba2/ffffff?text=Upload+or+YouTube+URL)

### AI Results
![Results](https://via.placeholder.com/800x450/ec4899/ffffff?text=AI-Generated+Results)

---

## 🎯 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                     INPUT OPTIONS                            │
├──────────────────────┬──────────────────────────────────────┤
│   Upload Video       │       YouTube URL                    │
│   📤 Drag & Drop     │       🎥 Paste Link                  │
└──────────┬───────────┴──────────────┬───────────────────────┘
           │                          │
           └──────────┬───────────────┘
                      ↓
           ┌──────────────────────┐
           │   AI Processing      │
           │   ⚙️ Transcribe      │
           │   🧠 Analyze         │
           │   ✂️ Generate Clips  │
           └──────────┬───────────┘
                      ↓
           ┌──────────────────────┐
           │   Results            │
           │   📝 Transcript      │
           │   📊 Summary         │
           │   🎬 Smart Clips     │
           │   📈 Analytics       │
           └──────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Authentication**: JWT with bcrypt
- **YouTube**: yt-dlp
- **AI**: OpenAI Whisper, Google Gemini
- **Server**: Gunicorn + Uvicorn

### Frontend
- **Design**: Modern glassmorphism
- **Animations**: CSS3 + JavaScript
- **Responsive**: Mobile-first approach
- **Icons**: Unicode emojis

### Deployment
- **Platform**: Render.com
- **CI/CD**: Automatic from GitHub
- **SSL**: Auto-provisioned
- **Storage**: 1GB included (free tier)

---

## 🔑 API Endpoints

### Authentication
```http
POST /api/auth/register
POST /api/auth/login
```

### Video Processing
```http
POST /api/videos/upload          # Direct upload
POST /api/videos/youtube          # YouTube URL
GET  /api/videos                  # List videos
GET  /api/videos/{id}/status      # Check progress
GET  /api/videos/{id}/transcript  # Get transcript
GET  /api/videos/{id}/summary     # Get summary
GET  /api/videos/{id}/clips       # Get clips
DELETE /api/videos/{id}           # Delete video
```

### Analytics
```http
GET /api/analytics/dashboard      # Get stats
```

### System
```http
GET /                            # API info
GET /health                      # Health check
GET /docs                        # Interactive docs
```

---

## 📖 API Documentation

Full interactive API documentation available at:
```
https://your-app.onrender.com/docs
```

### Example: Process YouTube Video

```javascript
// JavaScript example
const response = await fetch('https://your-app.onrender.com/api/videos/youtube', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    url: 'https://www.youtube.com/watch?v=VIDEO_ID',
    title: 'Machine Learning Basics',
    description: 'Introduction to ML concepts'
  })
});

const result = await response.json();
console.log(result.video_id); // Track this ID
```

### Example: Check Processing Status

```javascript
const status = await fetch(
  `https://your-app.onrender.com/api/videos/${videoId}/status`,
  {
    headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
  }
).then(r => r.json());

console.log(status.progress); // 0-100%
```

---

## 🎨 Customization

### Change Colors

Edit `index.html` CSS variables:

```css
:root {
    --primary: #6366f1;      /* Primary color */
    --secondary: #8b5cf6;    /* Secondary color */
    --accent: #ec4899;       /* Accent color */
    --success: #10b981;      /* Success color */
    /* ... */
}
```

### Add Your Logo

Replace the logo in navbar:

```html
<div class="logo">
    <img src="your-logo.png" alt="Logo">
    Your App Name
</div>
```

### Custom Domain

1. Add custom domain in Render dashboard
2. Update CNAME records in your DNS
3. SSL automatically provisioned

---

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `SECRET_KEY` | Yes | JWT secret key | - |
| `GEMINI_API_KEY` | No | Google Gemini API | None |
| `OPENAI_API_KEY` | No | OpenAI API key | None |
| `PORT` | No | Server port | 8000 |

### Storage Limits

**Free Tier:**
- Upload: 50MB per file
- Total: 1GB disk space
- Retention: Videos stored until deleted

**Paid Tier:**
- Upload: 500MB per file
- Total: 10GB+ disk space
- Retention: Unlimited

---

## 📊 Performance

### Free Tier Specifications
- **RAM**: 512MB
- **CPU**: Shared
- **Disk**: 1GB
- **Sleep**: After 15 min inactivity
- **Cold Start**: ~30 seconds

### Optimization Tips
1. Use YouTube URL for large videos
2. Delete old videos regularly
3. Consider paid plan for production
4. Enable keep-alive pings

---

## 🐛 Troubleshooting

### Issue: Deployment Failed

**Solution:**
```bash
# Check Render logs
# Verify requirements.txt format
# Ensure Python 3.11 compatibility
```

### Issue: YouTube Download Error

**Solution:**
- Verify video is public
- Check URL format
- Try different video
- Check Render logs

### Issue: Out of Storage

**Solution:**
```bash
# Delete old videos via API
DELETE /api/videos/{id}

# Or upgrade to paid plan
```

### Issue: Slow Processing

**Solution:**
- Free tier has limited resources
- Consider upgrading plan
- Use smaller videos for testing
- Check Render metrics

---

## 📈 Roadmap

### v2.1 (Coming Soon)
- [ ] Real-time collaborative editing
- [ ] Multi-language support (10+ languages)
- [ ] Advanced analytics dashboard
- [ ] Export to PowerPoint/PDF
- [ ] Mobile apps (iOS/Android)

### v2.2 (Future)
- [ ] Live streaming support
- [ ] AI-generated quizzes
- [ ] Voice cloning for narration
- [ ] AR/VR integration
- [ ] LMS integration (Moodle, Canvas)

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/educlip-ai-v2.git

# Install dev dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest

# Format code
black .

# Check linting
flake8
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the amazing framework
- [Render](https://render.com/) for simple deployment
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube support
- [OpenAI](https://openai.com/) for Whisper model
- [Google](https://ai.google.dev/) for Gemini API

---

## 📞 Support

- **Documentation**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Issues**: [GitHub Issues](https://github.com/yourusername/educlip-ai-v2/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/educlip-ai-v2/discussions)

---

## ⭐ Show Your Support

If you find this project helpful:
- ⭐ Star this repository
- 🐛 Report bugs
- 💡 Suggest features
- 🤝 Contribute code
- 📢 Share with others

---

## 📊 Project Stats

- **Lines of Code**: 2,000+
- **API Endpoints**: 15+
- **Supported Formats**: 5+ video formats
- **Deployment Time**: 3 minutes
- **Mobile Responsive**: ✅
- **Production Ready**: ✅

---

## 🎓 Use Cases

### Education
- Online courses
- Tutorial videos
- Lecture recordings
- Training materials

### Content Creation
- YouTube creators
- Course instructors
- Educational podcasters
- Video bloggers

### Enterprise
- Corporate training
- Employee onboarding
- Knowledge management
- Internal documentation

---

**Built with ❤️ for Education**

**Version**: 2.0.0  
**Status**: Production Ready ✅  
**Last Updated**: February 2026

---

[Get Started Now →](https://render.com/deploy?repo=https://github.com/yourusername/educlip-ai-v2)
