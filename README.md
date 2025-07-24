# 🤖 RAG Indexer Interface

A modern, feature-rich Retrieval Augmented Generation (RAG) system with Claude AI integration, local embeddings support, and a beautiful web interface. This project demonstrates how to build a complete RAG pipeline that can index documents, retrieve relevant content, generate AI-powered responses, and evaluate results.

**Author:** Gunnar MUC  
**Repository:** https://github.com/GunnarMUC/simple-rag-pipe  
**Enhanced by:** RAG-Indexer-Interface Team

![rag-image](./rag-design-basic.png)

## ✨ **New Features & Improvements**

### 🎨 **Modern Web Interface**
- **Dark/Light Mode Toggle** - Switch between themes seamlessly
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **Real-time Chat Interface** - Interactive conversation with AI
- **File Upload & Drag & Drop** - Easy document management
- **Live Statistics** - Real-time system monitoring
- **Beautiful Animations** - Smooth transitions and loading indicators

### 🔧 **Enhanced Backend**
- **Rate Limiting** - Protect against abuse with configurable limits
- **Comprehensive Logging** - Detailed logs for debugging and monitoring
- **Health Check Endpoints** - Monitor system status
- **Error Handling** - Graceful error management with user-friendly messages
- **Configuration Management** - Centralized settings with environment variables

### 🚀 **Deployment Ready**
- **Docker Support** - Easy containerized deployment
- **Docker Compose** - Multi-service orchestration
- **Production Configuration** - Optimized for production environments
- **Health Checks** - Automated system monitoring

## 🏗️ **Architecture**

### **Core Components**
- **Pipeline (`src/rag_pipeline.py`):** Orchestrates the entire RAG process
- **Datastore:** Manages embeddings and vector storage using LanceDB
- **Indexer:** Processes documents and creates data chunks using Docling
- **Retriever:** Searches the datastore with hybrid search capabilities
- **ResponseGenerator:** Generates answers using Claude AI with smart model selection
- **Evaluator:** Compares AI responses to expected answers

### **Web Interface**
- **Flask Backend:** RESTful API with rate limiting and security
- **Modern Frontend:** Responsive design with real-time updates
- **File Upload:** Drag & drop document processing
- **Live Statistics:** Real-time system monitoring

## 🚀 **Quick Start**

### **Option 1: Automated Setup (Recommended)**
```bash
# Clone the repository
git clone https://github.com/GunnarMUC/simple-rag-pipe.git RAG-Indexer-Interface
cd RAG-Indexer-Interface

# Run the automated setup
python dev_setup.py

# Update your API keys in .env file
# Then start the application
python app.py
```

### **Option 2: Manual Setup**
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
cp .env.example .env
# Edit .env file with your ANTHROPIC_API_KEY

# Start the application
python app.py
```

### **Option 3: Docker Deployment**
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t rag-indexer .
docker run -p 8080:8080 -e ANTHROPIC_API_KEY=your_key rag-indexer
```

## 🔧 **Configuration**

### **Environment Variables**
Create a `.env` file in the project root:

```sh
# Required
ANTHROPIC_API_KEY=your_claude_api_key_here

# Optional
CO_API_KEY=your_cohere_api_key_here
SECRET_KEY=your-secret-key-change-in-production

# Flask Settings
FLASK_DEBUG=True
HOST=0.0.0.0
PORT=8080

# Rate Limiting
RATE_LIMIT_ASK=10 per minute
RATE_LIMIT_UPLOAD=5 per minute

# Model Settings
EMBEDDING_MODEL=all-mpnet-base-v2
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
SIMILARITY_THRESHOLD=0.7
```

## 🌐 **Web Interface Features**

### **Chat Interface**
- **Real-time Conversations** - Interactive chat with AI
- **Message History** - View all questions and answers
- **Typing Indicators** - Visual feedback during processing
- **Error Handling** - Clear error messages and recovery

### **Document Management**
- **Drag & Drop Upload** - Easy file upload interface
- **Multiple File Support** - Upload multiple documents at once
- **Progress Tracking** - Real-time upload progress
- **File Validation** - Automatic format checking

### **System Monitoring**
- **Live Statistics** - Real-time document count and system status
- **Health Checks** - System health monitoring
- **Performance Metrics** - Response times and throughput

## 📊 **API Endpoints**

### **Core Endpoints**
- `GET /` - Main web interface
- `GET /health` - System health check
- `POST /api/ask` - Ask questions (rate limited)
- `POST /api/upload` - Upload documents (rate limited)
- `GET /api/stats` - System statistics

### **Advanced Endpoints**
- `POST /api/advanced` - Advanced search with metadata filtering

## 🧠 **Smart Model Selection**

The system automatically selects the most appropriate Claude model based on query type:

### **🤖 Claude Opus (Thinking Tasks)**
- **Use Case:** Complex analysis, reasoning, detailed explanations
- **Triggers:** Keywords like "why", "how", "explain", "analyze", "compare"
- **Cost:** $3/1M input, $15/1M output

### **💻 Claude Sonnet (Programming/General Tasks)**
- **Use Case:** Programming, technical queries, general questions
- **Triggers:** Keywords like "code", "function", "database", "implement"
- **Cost:** $3/1M input, $15/1M output

## 🐳 **Docker Deployment**

### **Development**
```bash
docker-compose up --build
```

### **Production**
```bash
# Use production profile
docker-compose --profile production up --build
```

### **Environment Variables**
```bash
# Set environment variables
export ANTHROPIC_API_KEY=your_key
export SECRET_KEY=your_secret

# Run with environment
docker-compose up
```

## 📁 **Project Structure**

```
RAG-Indexer-Interface/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── dev_setup.py           # Development setup script
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── templates/
│   └── index.html        # Modern web interface
├── src/
│   ├── rag_pipeline.py   # Core RAG pipeline
│   ├── impl/             # Implementation modules
│   └── interface/        # Abstract interfaces
├── sample_data/          # Sample documents and evaluations
├── data/                 # Vector database storage
├── uploads/              # File upload directory
└── logs/                 # Application logs
```

## 🧪 **Testing**

### **Run Tests**
```bash
# Basic functionality tests
python test_simple.py

# Model selection tests
python test_models.py

# Improvement tests
python test_improvements.py
```

### **Test Model Selection**
```bash
python test_models.py
```

## 🔍 **Usage Examples**

### **CLI Usage**
```bash
# Run the full pipeline
PYTHONPATH=src python3 main.py run

# Add documents
PYTHONPATH=src python3 main.py add -p "sample_data/source/"

# Query the database
PYTHONPATH=src python3 main.py query "What are the main attractions?"

# Evaluate the model
PYTHONPATH=src python3 main.py evaluate -f "sample_data/eval/sample_questions.json"
```

### **Web Interface**
1. **Upload Documents** - Use the drag & drop interface
2. **Ask Questions** - Type your questions in the chat
3. **View Responses** - Get AI-powered answers instantly
4. **Monitor System** - Check statistics and health status

## 📈 **Performance & Monitoring**

### **Rate Limiting**
- **Ask Questions:** 10 requests per minute
- **Upload Files:** 5 uploads per minute
- **General API:** 200 requests per day, 50 per hour

### **Health Monitoring**
- **Health Check:** `/health` endpoint
- **Statistics:** `/api/stats` endpoint
- **Logging:** Comprehensive application logs

## 🔒 **Security Features**

- **Rate Limiting** - Prevent abuse and ensure fair usage
- **Input Validation** - Sanitize all user inputs
- **Error Handling** - Graceful error management
- **Secure Headers** - Security headers for web interface
- **Environment Variables** - Secure configuration management

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License.

## 🙏 **Acknowledgments**

- **Original Author:** Gunnar MUC for the excellent RAG pipeline foundation
- **Claude AI:** For powerful language model capabilities
- **Sentence Transformers:** For efficient local embeddings
- **LanceDB:** For fast vector database operations

---

**Ready to get started?** Run `python dev_setup.py` and begin exploring your documents with AI-powered search!
