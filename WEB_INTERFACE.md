# 🌐 RAG Pipeline Web Interface

A simple browser-based interface for the RAG Pipeline that allows users to ask questions and get AI-powered responses.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Make sure your `.env` file contains your Claude API key:
```
ANTHROPIC_API_KEY=your_claude_api_key_here
```

### 3. Start the Web Server
```bash
python3 start_web.py
```

### 4. Open Your Browser
Navigate to: http://localhost:3000

## 🎯 Features

- **Simple Interface**: Clean, modern web interface
- **Real-time Responses**: Get answers instantly
- **Error Handling**: Graceful error messages
- **Loading States**: Visual feedback during processing
- **Mobile Friendly**: Responsive design

## 📝 Usage

1. **Ask Questions**: Type your question in the input field
2. **Get Answers**: Click "Ask Question" or press Enter
3. **View Results**: See the AI-generated response below

## 🔧 Technical Details

- **Backend**: Flask web server
- **Frontend**: HTML/CSS/JavaScript
- **AI**: Claude API for text generation
- **Embeddings**: Local sentence-transformers
- **Database**: LanceDB for vector storage

## 🛠️ Customization

### Change Port
Edit `app.py` and modify the port in the last line:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change 3000 to your preferred port
```

### Modify Styling
Edit `templates/index.html` to customize the appearance.

### Add More Features
- Multiple responses
- Response history
- File upload for new documents
- Export conversations

## 🐛 Troubleshooting

### "Module not found" errors
Make sure you're running from the project root directory.

### API key errors
Verify your `.env` file contains the correct ANTHROPIC_API_KEY.

### Port already in use
Change the port number in `app.py` or stop other services using port 3000.

## 📊 Performance

- **First Query**: May take 10-15 seconds (initializes pipeline)
- **Subsequent Queries**: 2-5 seconds per question
- **Memory Usage**: ~500MB (includes sentence-transformers model)

## 🔒 Security

- No data is stored permanently
- API keys are kept server-side only
- HTTPS recommended for production use 