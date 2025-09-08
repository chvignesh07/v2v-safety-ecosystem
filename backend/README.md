# Backend

This directory contains the backend components of the V2V Safety Ecosystem.

## Architecture Overview

The backend is built with Flask and follows a modular architecture:

### Core Components

- **`app.py`** - Main Flask application with SocketIO support
- **`requirements.txt`** - Python dependencies
- **`README.md`** - This documentation

### Module Structure

#### `/api` - API Endpoints Module
- **`health.py`** - Health check endpoints for system monitoring
- **`routes.py`** - V2V communication API routes

#### `/rl_engine` - Reinforcement Learning Module  
- **`__init__.py`** - RL engine initialization and configuration
- Core RL functionality for safety decision making
- Includes Q-learning and DQN algorithms
- Environment interaction and policy optimization

#### `/sockets` - Socket.IO Communication Module
- **`__init__.py`** - WebSocket configuration and namespaces
- Real-time V2V communication infrastructure
- Event-driven messaging system
- Room-based vehicle clustering

## Features

The backend provides:

- **RESTful API endpoints** for V2V communication
- **Real-time WebSocket messaging** for instant safety alerts
- **Reinforcement learning engine** for intelligent decision making
- **Health monitoring** for system diagnostics
- **Modular architecture** for easy extension and maintenance

## Getting Started

### Prerequisites
- Python 3.8+
- Flask
- Flask-SocketIO
- Additional dependencies listed in `requirements.txt`

### Installation
```bash
cd backend
pip install -r requirements.txt
```

### Running the Application
```bash
python app.py
```

The application will start on `http://localhost:5000` by default.

### API Endpoints

- **Health Check**: `GET /health` - System health status
- **V2V Routes**: See `/api/routes.py` for complete endpoint documentation

### WebSocket Namespaces

- `/v2v` - Vehicle-to-Vehicle communication
- `/safety` - Safety alert broadcasts  
- `/admin` - Administrative controls
- `/monitor` - System monitoring

## Development Status

✅ **Completed (Step 2.1)**:
- Flask app structure with SocketIO
- API module with health checks
- RL engine module foundation
- Sockets module for real-time communication
- Modular architecture setup

🔄 **In Progress**:
- Individual module implementations
- Database integration
- Authentication system
- Comprehensive testing

## Contributing

See the main project README for contribution guidelines.
