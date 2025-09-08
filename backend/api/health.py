"""Health Check API Module for V2V Safety Ecosystem

This module provides health check endpoints for monitoring the backend service.
It includes system status, dependencies health, and performance metrics.

Author: V2V Safety Team
Date: September 7, 2025
Version: 1.0.0
"""

from flask import Blueprint, jsonify, request
import psutil
import datetime
import logging
import time
import os

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
health_bp = Blueprint('health', __name__)

# Global variables for health tracking
service_start_time = datetime.datetime.now()
health_checks_count = 0

@health_bp.route('/', methods=['GET'])
@health_bp.route('/status', methods=['GET'])
def health_check():
    """Simple health check endpoint.
    
    Returns:
        dict: Basic service status information
    """
    global health_checks_count
    health_checks_count += 1
    
    return jsonify({
        'status': 'healthy',
        'service': 'V2V Safety Ecosystem Backend',
        'version': '1.0.0',
        'timestamp': datetime.datetime.now().isoformat(),
        'uptime_seconds': (datetime.datetime.now() - service_start_time).total_seconds(),
        'health_checks_performed': health_checks_count
    }), 200

@health_bp.route('/detailed', methods=['GET'])
def detailed_health_check():
    """Detailed health check with system metrics.
    
    Returns:
        dict: Comprehensive system health information
    """
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Process metrics
        process = psutil.Process(os.getpid())
        process_memory = process.memory_info()
        
        uptime = datetime.datetime.now() - service_start_time
        
        health_data = {
            'status': 'healthy',
            'service': 'V2V Safety Ecosystem Backend',
            'version': '1.0.0',
            'timestamp': datetime.datetime.now().isoformat(),
            'uptime': {
                'seconds': uptime.total_seconds(),
                'formatted': str(uptime)
            },
            'system_metrics': {
                'cpu_percent': cpu_percent,
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'percent': memory.percent,
                    'used': memory.used
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': (disk.used / disk.total) * 100
                }
            },
            'process_metrics': {
                'memory_rss': process_memory.rss,
                'memory_vms': process_memory.vms,
                'cpu_percent': process.cpu_percent(),
                'num_threads': process.num_threads(),
                'pid': os.getpid()
            },
            'environment': {
                'python_version': os.sys.version,
                'platform': os.name
            },
            'health_checks_performed': health_checks_count
        }
        
        # Determine overall health status
        if cpu_percent > 90 or memory.percent > 90:
            health_data['status'] = 'warning'
            health_data['warnings'] = []
            if cpu_percent > 90:
                health_data['warnings'].append('High CPU usage detected')
            if memory.percent > 90:
                health_data['warnings'].append('High memory usage detected')
        
        return jsonify(health_data), 200
        
    except Exception as e:
        logger.error(f"Error in detailed health check: {str(e)}")
        return jsonify({
            'status': 'error',
            'service': 'V2V Safety Ecosystem Backend',
            'timestamp': datetime.datetime.now().isoformat(),
            'error': 'Failed to retrieve system metrics',
            'details': str(e)
        }), 500

@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    """Kubernetes readiness probe endpoint.
    
    Returns:
        dict: Service readiness status
    """
    try:
        # Add checks for critical dependencies here
        # For now, basic check
        
        checks = {
            'flask_app': True,  # If we're responding, Flask is working
            'socketio': True,   # TODO: Add actual SocketIO check
            'database': True,   # TODO: Add database connectivity check
        }
        
        all_ready = all(checks.values())
        
        return jsonify({
            'ready': all_ready,
            'service': 'V2V Safety Ecosystem Backend',
            'timestamp': datetime.datetime.now().isoformat(),
            'checks': checks
        }), 200 if all_ready else 503
        
    except Exception as e:
        logger.error(f"Error in readiness check: {str(e)}")
        return jsonify({
            'ready': False,
            'service': 'V2V Safety Ecosystem Backend',
            'timestamp': datetime.datetime.now().isoformat(),
            'error': str(e)
        }), 503

@health_bp.route('/live', methods=['GET'])
def liveness_check():
    """Kubernetes liveness probe endpoint.
    
    Returns:
        dict: Service liveness status
    """
    return jsonify({
        'alive': True,
        'service': 'V2V Safety Ecosystem Backend',
        'timestamp': datetime.datetime.now().isoformat(),
        'uptime_seconds': (datetime.datetime.now() - service_start_time).total_seconds()
    }), 200

@health_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors in health blueprint."""
    return jsonify({
        'error': 'Health endpoint not found',
        'message': 'Available endpoints: /, /status, /detailed, /ready, /live'
    }), 404

@health_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors in health blueprint."""
    logger.error(f"Internal error in health check: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'Health check service encountered an error'
    }), 500
