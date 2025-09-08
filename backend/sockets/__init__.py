"""
Socket.IO Communication Module

This module provides real-time communication capabilities for the V2V Safety Ecosystem
using Flask-SocketIO, including:
- WebSocket connection management
- Real-time data streaming between vehicles
- Event-driven communication handlers
- Room-based messaging for vehicle clusters
- Broadcasting safety alerts and updates

Author: V2V Safety Ecosystem Team
Created: September 2025
"""

from .handlers import SocketHandlers
from .events import V2VEvents
from .rooms import RoomManager
from .auth import SocketAuth
from .utils import SocketUtils

__version__ = "1.0.0"
__all__ = [
    "SocketHandlers",
    "V2VEvents",
    "RoomManager",
    "SocketAuth",
    "SocketUtils"
]

# Socket.IO configuration
SOCKET_CONFIG = {
    "cors_allowed_origins": "*",
    "async_mode": "threading",
    "ping_timeout": 60,
    "ping_interval": 25,
    "logger": True,
    "engineio_logger": True
}

# Event namespaces
NAMESPACES = {
    "v2v": "/v2v",           # Vehicle-to-Vehicle communication
    "safety": "/safety",   # Safety alert broadcasts
    "admin": "/admin",     # Administrative controls
    "monitor": "/monitor"  # System monitoring
}

def get_version():
    """Return the current version of the sockets module."""
    return __version__

def get_socket_config():
    """Return the default Socket.IO configuration."""
    return SOCKET_CONFIG.copy()

def get_namespaces():
    """Return the available Socket.IO namespaces."""
    return NAMESPACES.copy()
