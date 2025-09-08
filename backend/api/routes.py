"""Main API Routes Module for V2V Safety Ecosystem

This module contains the primary API endpoints for vehicle-to-vehicle communication,
safety alerts, and real-time data exchange in the V2V Safety Ecosystem.

Author: V2V Safety Team
Date: September 7, 2025
Version: 1.0.0
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
import uuid
import json
from typing import Dict, List, Any

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__)

# In-memory storage for development (replace with database in production)
vehicle_registry = {}
safety_alerts = []
communication_logs = []

# Helper functions
def validate_vehicle_data(data: Dict[str, Any]) -> tuple:
    """Validate vehicle registration data.
    
    Args:
        data: Vehicle data dictionary
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = ['vehicle_id', 'position', 'speed', 'heading']
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate position format
    if not isinstance(data['position'], dict) or 'lat' not in data['position'] or 'lon' not in data['position']:
        return False, "Position must contain 'lat' and 'lon' coordinates"
    
    return True, None

def create_api_response(success: bool, data: Any = None, message: str = None, status_code: int = 200) -> tuple:
    """Create standardized API response.
    
    Args:
        success: Success status
        data: Response data
        message: Response message
        status_code: HTTP status code
        
    Returns:
        tuple: (response_dict, status_code)
    """
    response = {
        'success': success,
        'timestamp': datetime.now().isoformat(),
        'message': message
    }
    
    if data is not None:
        response['data'] = data
        
    return jsonify(response), status_code

# Vehicle Registration and Management Endpoints
@api_bp.route('/vehicles/register', methods=['POST'])
def register_vehicle():
    """Register a new vehicle in the V2V network.
    
    Expected JSON payload:
    {
        "vehicle_id": "string",
        "position": {"lat": float, "lon": float},
        "speed": float,
        "heading": float,
        "vehicle_type": "string",
        "capabilities": ["string"]
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return create_api_response(False, message="No JSON data provided", status_code=400)
        
        # Validate required fields
        is_valid, error_msg = validate_vehicle_data(data)
        if not is_valid:
            return create_api_response(False, message=error_msg, status_code=400)
        
        vehicle_id = data['vehicle_id']
        
        # Create vehicle registration record
        vehicle_record = {
            'vehicle_id': vehicle_id,
            'position': data['position'],
            'speed': data['speed'],
            'heading': data['heading'],
            'vehicle_type': data.get('vehicle_type', 'unknown'),
            'capabilities': data.get('capabilities', []),
            'registered_at': datetime.now().isoformat(),
            'last_update': datetime.now().isoformat(),
            'status': 'active'
        }
        
        # Store in registry
        vehicle_registry[vehicle_id] = vehicle_record
        
        logger.info(f"Vehicle {vehicle_id} registered successfully")
        
        return create_api_response(
            True, 
            data={'vehicle_id': vehicle_id, 'status': 'registered'},
            message="Vehicle registered successfully"
        )
        
    except Exception as e:
        logger.error(f"Error registering vehicle: {str(e)}")
        return create_api_response(False, message="Internal server error", status_code=500)

@api_bp.route('/vehicles/<vehicle_id>/update', methods=['PUT'])
def update_vehicle_status(vehicle_id: str):
    """Update vehicle position and status.
    
    Args:
        vehicle_id: Unique vehicle identifier
    """
    try:
        if vehicle_id not in vehicle_registry:
            return create_api_response(False, message="Vehicle not found", status_code=404)
        
        data = request.get_json()
        if not data:
            return create_api_response(False, message="No JSON data provided", status_code=400)
        
        # Update vehicle record
        vehicle = vehicle_registry[vehicle_id]
        
        # Update position if provided
        if 'position' in data:
            vehicle['position'] = data['position']
        
        # Update other fields
        updateable_fields = ['speed', 'heading', 'status']
        for field in updateable_fields:
            if field in data:
                vehicle[field] = data[field]
        
        vehicle['last_update'] = datetime.now().isoformat()
        
        logger.info(f"Vehicle {vehicle_id} status updated")
        
        return create_api_response(
            True,
            data={'vehicle_id': vehicle_id, 'last_update': vehicle['last_update']},
            message="Vehicle status updated successfully"
        )
        
    except Exception as e:
        logger.error(f"Error updating vehicle {vehicle_id}: {str(e)}")
        return create_api_response(False, message="Internal server error", status_code=500)

@api_bp.route('/vehicles', methods=['GET'])
def get_vehicles():
    """Get list of all registered vehicles."""
    try:
        # Filter query parameters
        status_filter = request.args.get('status')
        vehicle_type_filter = request.args.get('type')
        
        vehicles = list(vehicle_registry.values())
        
        # Apply filters
        if status_filter:
            vehicles = [v for v in vehicles if v.get('status') == status_filter]
            
        if vehicle_type_filter:
            vehicles = [v for v in vehicles if v.get('vehicle_type') == vehicle_type_filter]
        
        return create_api_response(
            True,
            data={
                'vehicles': vehicles,
                'count': len(vehicles),
                'filters_applied': {
                    'status': status_filter,
                    'type': vehicle_type_filter
                }
            },
            message="Vehicles retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Error retrieving vehicles: {str(e)}")
        return create_api_response(False, message="Internal server error", status_code=500)

# Safety Alert Endpoints
@api_bp.route('/safety/alerts', methods=['POST'])
def create_safety_alert():
    """Create a new safety alert.
    
    Expected JSON payload:
    {
        "alert_type": "string",
        "severity": "low|medium|high|critical",
        "position": {"lat": float, "lon": float},
        "radius": float,
        "message": "string",
        "vehicle_id": "string"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return create_api_response(False, message="No JSON data provided", status_code=400)
        
        # Validate required fields
        required_fields = ['alert_type', 'severity', 'position', 'message', 'vehicle_id']
        for field in required_fields:
            if field not in data:
                return create_api_response(False, message=f"Missing required field: {field}", status_code=400)
        
        # Create alert record
        alert_id = str(uuid.uuid4())
        alert_record = {
            'alert_id': alert_id,
            'alert_type': data['alert_type'],
            'severity': data['severity'],
            'position': data['position'],
            'radius': data.get('radius', 100),  # Default 100m radius
            'message': data['message'],
            'source_vehicle_id': data['vehicle_id'],
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'acknowledged_by': []
        }
        
        # Store alert
        safety_alerts.append(alert_record)
        
        logger.info(f"Safety alert {alert_id} created by vehicle {data['vehicle_id']}")
        
        # TODO: Implement real-time broadcast to nearby vehicles via SocketIO
        
        return create_api_response(
            True,
            data={'alert_id': alert_id, 'status': 'created'},
            message="Safety alert created successfully"
        )
        
    except Exception as e:
        logger.error(f"Error creating safety alert: {str(e)}")
        return create_api_response(False, message="Internal server error", status_code=500)

@api_bp.route('/safety/alerts', methods=['GET'])
def get_safety_alerts():
    """Get safety alerts, optionally filtered by location and severity."""
    try:
        # Query parameters
        severity_filter = request.args.get('severity')
        alert_type_filter = request.args.get('type')
        status_filter = request.args.get('status', 'active')
        
        # Filter alerts
        filtered_alerts = safety_alerts.copy()
        
        if severity_filter:
            filtered_alerts = [a for a in filtered_alerts if a.get('severity') == severity_filter]
            
        if alert_type_filter:
            filtered_alerts = [a for a in filtered_alerts if a.get('alert_type') == alert_type_filter]
            
        if status_filter:
            filtered_alerts = [a for a in filtered_alerts if a.get('status') == status_filter]
        
        # Sort by creation time (newest first)
        filtered_alerts.sort(key=lambda x: x['created_at'], reverse=True)
        
        return create_api_response(
            True,
            data={
                'alerts': filtered_alerts,
                'count': len(filtered_alerts),
                'filters_applied': {
                    'severity': severity_filter,
                    'type': alert_type_filter,
                    'status': status_filter
                }
            },
            message="Safety alerts retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Error retrieving safety alerts: {str(e)}")
        return create_api_response(False, message="Internal server error", status_code=500)

# Communication and Messaging Endpoints
@api_bp.route('/communication/send', methods=['POST'])
def send_v2v_message():
    """Send a V2V communication message.
    
    Expected JSON payload:
    {
        "sender_id": "string",
        "recipient_id": "string" | "broadcast",
        "message_type": "string",
        "payload": object,
        "priority": "low|medium|high"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return create_api_response(False, message="No JSON data provided", status_code=400)
        
        # Validate required fields
        required_fields = ['sender_id', 'recipient_id', 'message_type', 'payload']
        for field in required_fields:
            if field not in data:
                return create_api_response(False, message=f"Missing required field: {field}", status_code=400)
        
        # Create message record
        message_id = str(uuid.uuid4())
        message_record = {
            'message_id': message_id,
            'sender_id': data['sender_id'],
            'recipient_id': data['recipient_id'],
            'message_type': data['message_type'],
            'payload': data['payload'],
            'priority': data.get('priority', 'medium'),
            'timestamp': datetime.now().isoformat(),
            'status': 'sent'
        }
        
        # Store communication log
        communication_logs.append(message_record)
        
        logger.info(f"V2V message {message_id} sent from {data['sender_id']} to {data['recipient_id']}")
        
        # TODO: Implement actual message delivery via SocketIO
        
        return create_api_response(
            True,
            data={'message_id': message_id, 'status': 'sent'},
            message="V2V message sent successfully"
        )
        
    except Exception as e:
        logger.error(f"Error sending V2V message: {str(e)}")
        return create_api_response(False, message="Internal server error", status_code=500)

# Error Handlers
@api_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return create_api_response(False, message="API endpoint not found", status_code=404)

@api_bp.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return create_api_response(False, message="Method not allowed for this endpoint", status_code=405)

@api_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return create_api_response(False, message="Internal server error", status_code=500)
