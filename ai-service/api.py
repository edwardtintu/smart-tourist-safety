"""
Flask API for Tourist Anomaly Detection Service
Provides REST endpoints for real-time anomaly detection
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import pandas as pd
import os
import json
from anomaly import TouristAnomalyDetector

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global anomaly detector instance
detector = TouristAnomalyDetector()

# In-memory storage for tourist historical data (for demo purposes)
# In production, this would be a proper database
tourist_history = {}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Tourist Anomaly Detection API',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'version': '1.0.0'
    })

@app.route('/check_anomaly', methods=['POST'])
def check_anomaly():
    """
    Check for anomalies in tourist movement
    
    Expected JSON input:
    {
        "tourist_id": 1,
        "lat": 12.9716,
        "lon": 77.5946,
        "timestamp": "2024-01-15T10:30:00"
    }
    
    Returns:
    {
        "status": "normal" | "anomaly",
        "anomalies": [...],
        "tourist_id": 1,
        "timestamp": "2024-01-15T10:30:00"
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                'error': 'Request must be JSON',
                'status': 'error'
            }), 400
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['tourist_id', 'lat', 'lon', 'timestamp']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'status': 'error'
                }), 400
        
        # Extract data
        tourist_id = data['tourist_id']
        lat = float(data['lat'])
        lon = float(data['lon'])
        timestamp = data['timestamp']
        
        # Validate coordinates
        if not (-90 <= lat <= 90):
            return jsonify({
                'error': 'Invalid latitude. Must be between -90 and 90',
                'status': 'error'
            }), 400
        
        if not (-180 <= lon <= 180):
            return jsonify({
                'error': 'Invalid longitude. Must be between -180 and 180',
                'status': 'error'
            }), 400
        
        # Validate timestamp format
        try:
            datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            try:
                datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return jsonify({
                    'error': 'Invalid timestamp format. Use YYYY-MM-DDTHH:MM:SS or YYYY-MM-DD HH:MM:SS',
                    'status': 'error'
                }), 400
        
        # Get historical data for this tourist
        historical_data = None
        if tourist_id in tourist_history:
            historical_data = pd.DataFrame(tourist_history[tourist_id])
        
        # Check for anomalies
        anomalies = detector.check_single_point(
            tourist_id=tourist_id,
            lat=lat,
            lon=lon,
            timestamp=timestamp,
            historical_data=historical_data
        )
        
        # Store this point in history
        if tourist_id not in tourist_history:
            tourist_history[tourist_id] = []
        
        tourist_history[tourist_id].append({
            'tourist_id': tourist_id,
            'lat': lat,
            'lon': lon,
            'timestamp': timestamp,
            'is_anomaly': len(anomalies) > 0,
            'anomaly_type': anomalies[0]['anomaly_type'] if anomalies else 'normal'
        })
        
        # Keep only last 100 points per tourist (memory management)
        if len(tourist_history[tourist_id]) > 100:
            tourist_history[tourist_id] = tourist_history[tourist_id][-100:]
        
        # Prepare response
        status = 'anomaly' if anomalies else 'normal'
        
        response = {
            'status': status,
            'tourist_id': tourist_id,
            'timestamp': timestamp,
            'location': {
                'lat': lat,
                'lon': lon
            },
            'anomalies': []
        }
        
        # Add anomaly details
        for anomaly in anomalies:
            response['anomalies'].append({
                'type': anomaly['anomaly_type'],
                'reason': anomaly['details'],
                'confidence': round(anomaly['confidence'], 2)
            })
        
        # Add summary reason for first anomaly
        if anomalies:
            response['reason'] = anomalies[0]['details']
        
        return jsonify(response)
    
    except ValueError as e:
        return jsonify({
            'error': f'Invalid data format: {str(e)}',
            'status': 'error'
        }), 400
    
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/analyze_batch', methods=['POST'])
def analyze_batch():
    """
    Analyze a batch of tourist data for anomalies
    
    Expected JSON input:
    {
        "data": [
            {"tourist_id": 1, "lat": 12.9716, "lon": 77.5946, "timestamp": "2024-01-15T10:30:00"},
            {"tourist_id": 1, "lat": 12.9726, "lon": 77.5956, "timestamp": "2024-01-15T10:31:00"},
            ...
        ]
    }
    """
    try:
        if not request.is_json:
            return jsonify({
                'error': 'Request must be JSON',
                'status': 'error'
            }), 400
        
        request_data = request.get_json()
        
        if 'data' not in request_data:
            return jsonify({
                'error': 'Missing "data" field',
                'status': 'error'
            }), 400
        
        # Convert to DataFrame
        df = pd.DataFrame(request_data['data'])
        
        # Validate required columns
        required_columns = ['tourist_id', 'lat', 'lon', 'timestamp']
        for col in required_columns:
            if col not in df.columns:
                return jsonify({
                    'error': f'Missing required column: {col}',
                    'status': 'error'
                }), 400
        
        # Analyze for anomalies
        anomalies = detector.analyze_tourist_data(df, use_ml=True)
        
        # Prepare response
        response = {
            'status': 'success',
            'total_points': len(df),
            'anomalies_detected': len(anomalies),
            'anomalies': []
        }
        
        for anomaly in anomalies:
            response['anomalies'].append({
                'tourist_id': anomaly['tourist_id'],
                'timestamp': anomaly['timestamp'],
                'location': {
                    'lat': anomaly['lat'],
                    'lon': anomaly['lon']
                },
                'type': anomaly['anomaly_type'],
                'reason': anomaly['details'],
                'confidence': round(anomaly['confidence'], 2)
            })
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/tourist_history/<int:tourist_id>', methods=['GET'])
def get_tourist_history(tourist_id):
    """Get historical data for a specific tourist"""
    if tourist_id not in tourist_history:
        return jsonify({
            'error': 'Tourist not found',
            'status': 'error'
        }), 404
    
    return jsonify({
        'tourist_id': tourist_id,
        'history': tourist_history[tourist_id],
        'total_points': len(tourist_history[tourist_id])
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get service statistics"""
    total_tourists = len(tourist_history)
    total_points = sum(len(history) for history in tourist_history.values())
    
    anomaly_count = 0
    for history in tourist_history.values():
        anomaly_count += sum(1 for point in history if point['is_anomaly'])
    
    return jsonify({
        'total_tourists': total_tourists,
        'total_data_points': total_points,
        'total_anomalies': anomaly_count,
        'anomaly_rate': round(anomaly_count / max(total_points, 1) * 100, 2),
        'service_uptime': 'Active'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500

def load_sample_data():
    """Load sample data if available"""
    try:
        csv_path = 'tourist_data.csv'
        if os.path.exists(csv_path):
            print("Loading sample data for ML model training...")
            df = pd.read_csv(csv_path)
            detector.analyze_tourist_data(df, use_ml=True)
            print("Sample data loaded and ML model trained")
        else:
            print("No sample data found. ML model will be trained on-demand.")
    except Exception as e:
        print(f"Error loading sample data: {e}")

if __name__ == '__main__':
    print("Starting Tourist Anomaly Detection API...")
    print("Loading configuration...")
    
    # Load sample data for ML training
    load_sample_data()
    
    print("API Server starting on http://localhost:5001")
    print("\nAvailable endpoints:")
    print("  GET  /health - Health check")
    print("  POST /check_anomaly - Check single GPS point")
    print("  POST /analyze_batch - Analyze batch of data")
    print("  GET  /tourist_history/<id> - Get tourist history")
    print("  GET  /stats - Service statistics")
    print("\nExample request:")
    print('  curl -X POST http://localhost:5001/check_anomaly \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"tourist_id":1,"lat":12.9716,"lon":77.5946,"timestamp":"2024-01-15T10:30:00"}\'')
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5001, debug=True)
