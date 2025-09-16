"""
Anomaly Detection Module
Implements rule-based and ML-based anomaly detection for tourist movement
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class TouristAnomalyDetector:
    def __init__(self, stop_threshold_minutes=5, deviation_threshold_meters=200):
        self.stop_threshold_minutes = stop_threshold_minutes
        self.deviation_threshold_meters = deviation_threshold_meters
        
        # Planned route (same as in data_sim.py)
        self.planned_route = [
            (12.9716, 77.5946),  # Start point
            (12.9726, 77.5956),  # Point 2
            (12.9736, 77.5966),  # Point 3
            (12.9746, 77.5976),  # Point 4
            (12.9756, 77.5986),  # End point
        ]
        
        # ML model for pattern-based detection
        self.ml_model = None
        self.scaler = StandardScaler()
        
    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two GPS points in meters"""
        R = 6371000  # Earth's radius in meters
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def detect_stop_anomaly(self, df, tourist_id):
        """Detect if tourist has stopped for too long"""
        tourist_data = df[df['tourist_id'] == tourist_id].copy()
        tourist_data = tourist_data.sort_values('timestamp')
        
        anomalies = []
        
        if len(tourist_data) < 2:
            return anomalies
        
        # Convert timestamps to datetime
        tourist_data['datetime'] = pd.to_datetime(tourist_data['timestamp'])
        
        # Check consecutive points for stops
        for i in range(1, len(tourist_data)):
            current_row = tourist_data.iloc[i]
            prev_row = tourist_data.iloc[i-1]
            
            # Calculate distance between consecutive points
            distance = self.haversine_distance(
                prev_row['lat'], prev_row['lon'],
                current_row['lat'], current_row['lon']
            )
            
            # Calculate time difference
            time_diff = (current_row['datetime'] - prev_row['datetime']).total_seconds() / 60
            
            # If distance is very small and time is significant, it's a stop
            if distance < 10 and time_diff >= self.stop_threshold_minutes:  # 10 meters threshold
                anomalies.append({
                    'tourist_id': tourist_id,
                    'timestamp': current_row['timestamp'],
                    'lat': current_row['lat'],
                    'lon': current_row['lon'],
                    'anomaly_type': 'stopped_too_long',
                    'details': f'Stopped for {time_diff:.1f} minutes',
                    'confidence': min(time_diff / self.stop_threshold_minutes, 2.0)
                })
        
        return anomalies
    
    def detect_route_deviation(self, df, tourist_id):
        """Detect if tourist has deviated from planned route"""
        tourist_data = df[df['tourist_id'] == tourist_id].copy()
        anomalies = []
        
        for _, row in tourist_data.iterrows():
            # Find minimum distance to planned route
            min_distance = float('inf')
            
            # Check distance to each segment of the planned route
            for i in range(len(self.planned_route) - 1):
                start_point = self.planned_route[i]
                end_point = self.planned_route[i + 1]
                
                # Distance to start point
                dist_start = self.haversine_distance(
                    row['lat'], row['lon'], start_point[0], start_point[1]
                )
                
                # Distance to end point
                dist_end = self.haversine_distance(
                    row['lat'], row['lon'], end_point[0], end_point[1]
                )
                
                # Distance to line segment (simplified)
                min_distance = min(min_distance, dist_start, dist_end)
            
            # Check if deviation exceeds threshold
            if min_distance > self.deviation_threshold_meters:
                anomalies.append({
                    'tourist_id': tourist_id,
                    'timestamp': row['timestamp'],
                    'lat': row['lat'],
                    'lon': row['lon'],
                    'anomaly_type': 'route_deviation',
                    'details': f'Deviated {min_distance:.0f}m from planned route',
                    'confidence': min(min_distance / self.deviation_threshold_meters, 3.0)
                })
        
        return anomalies
    
    def prepare_ml_features(self, df):
        """Prepare features for ML-based anomaly detection"""
        features = []
        
        for tourist_id in df['tourist_id'].unique():
            tourist_data = df[df['tourist_id'] == tourist_id].copy()
            tourist_data = tourist_data.sort_values('timestamp')
            tourist_data['datetime'] = pd.to_datetime(tourist_data['timestamp'])
            
            for i in range(1, len(tourist_data)):
                current_row = tourist_data.iloc[i]
                prev_row = tourist_data.iloc[i-1]
                
                # Calculate movement features
                distance = self.haversine_distance(
                    prev_row['lat'], prev_row['lon'],
                    current_row['lat'], current_row['lon']
                )
                
                time_diff = (current_row['datetime'] - prev_row['datetime']).total_seconds() / 60
                speed = distance / max(time_diff, 0.1)  # meters per minute
                
                # Distance from route center
                route_center_lat = np.mean([p[0] for p in self.planned_route])
                route_center_lon = np.mean([p[1] for p in self.planned_route])
                
                distance_from_center = self.haversine_distance(
                    current_row['lat'], current_row['lon'],
                    route_center_lat, route_center_lon
                )
                
                features.append([
                    distance,           # Movement distance
                    time_diff,         # Time between points
                    speed,             # Movement speed
                    distance_from_center,  # Distance from route center
                    current_row['lat'],    # Latitude
                    current_row['lon']     # Longitude
                ])
        
        return np.array(features)
    
    def train_ml_model(self, df):
        """Train ML model for pattern-based anomaly detection"""
        print("Training ML model for anomaly detection...")
        
        # Prepare features
        features = self.prepare_ml_features(df)
        
        if len(features) == 0:
            print("No features available for training")
            return
        
        # Scale features
        features_scaled = self.scaler.fit_transform(features)
        
        # Train Isolation Forest
        self.ml_model = IsolationForest(
            contamination=0.1,  # Expect 10% anomalies
            random_state=42,
            n_estimators=100
        )
        
        self.ml_model.fit(features_scaled)
        print("ML model training completed")
    
    def detect_ml_anomalies(self, df):
        """Detect anomalies using trained ML model"""
        if self.ml_model is None:
            return []
        
        features = self.prepare_ml_features(df)
        if len(features) == 0:
            return []
        
        features_scaled = self.scaler.transform(features)
        predictions = self.ml_model.predict(features_scaled)
        anomaly_scores = self.ml_model.decision_function(features_scaled)
        
        anomalies = []
        feature_idx = 0
        
        for tourist_id in df['tourist_id'].unique():
            tourist_data = df[df['tourist_id'] == tourist_id].copy()
            tourist_data = tourist_data.sort_values('timestamp')
            
            for i in range(1, len(tourist_data)):
                if feature_idx < len(predictions) and predictions[feature_idx] == -1:
                    current_row = tourist_data.iloc[i]
                    anomalies.append({
                        'tourist_id': tourist_id,
                        'timestamp': current_row['timestamp'],
                        'lat': current_row['lat'],
                        'lon': current_row['lon'],
                        'anomaly_type': 'ml_pattern_anomaly',
                        'details': f'ML detected unusual pattern (score: {anomaly_scores[feature_idx]:.2f})',
                        'confidence': abs(anomaly_scores[feature_idx])
                    })
                feature_idx += 1
        
        return anomalies
    
    def analyze_tourist_data(self, df, use_ml=True):
        """Complete anomaly analysis for tourist data"""
        all_anomalies = []
        
        # Rule-based detection
        for tourist_id in df['tourist_id'].unique():
            # Detect stops
            stop_anomalies = self.detect_stop_anomaly(df, tourist_id)
            all_anomalies.extend(stop_anomalies)
            
            # Detect route deviations
            deviation_anomalies = self.detect_route_deviation(df, tourist_id)
            all_anomalies.extend(deviation_anomalies)
        
        # ML-based detection (optional)
        if use_ml:
            try:
                self.train_ml_model(df)
                ml_anomalies = self.detect_ml_anomalies(df)
                all_anomalies.extend(ml_anomalies)
            except Exception as e:
                print(f"ML detection failed: {e}")
        
        return all_anomalies
    
    def check_single_point(self, tourist_id, lat, lon, timestamp, historical_data=None):
        """Check a single GPS point for anomalies (for real-time API)"""
        anomalies = []
        
        # Create a temporary dataframe for this point
        current_point = pd.DataFrame([{
            'tourist_id': tourist_id,
            'lat': lat,
            'lon': lon,
            'timestamp': timestamp,
            'is_anomaly': False,
            'anomaly_type': 'unknown'
        }])
        
        # Check route deviation
        deviation_anomalies = self.detect_route_deviation(current_point, tourist_id)
        anomalies.extend(deviation_anomalies)
        
        # If historical data is provided, check for stops
        if historical_data is not None and len(historical_data) > 0:
            # Combine with historical data
            combined_data = pd.concat([historical_data, current_point], ignore_index=True)
            stop_anomalies = self.detect_stop_anomaly(combined_data, tourist_id)
            
            # Only return anomalies for the current point
            current_time = pd.to_datetime(timestamp)
            for anomaly in stop_anomalies:
                anomaly_time = pd.to_datetime(anomaly['timestamp'])
                if abs((current_time - anomaly_time).total_seconds()) < 60:  # Within 1 minute
                    anomalies.append(anomaly)
        
        return anomalies

def main():
    """Test the anomaly detection system"""
    print("Testing Anomaly Detection System...")
    
    # Load data
    try:
        df = pd.read_csv('tourist_data.csv')
        print(f"Loaded {len(df)} data points")
    except FileNotFoundError:
        print("tourist_data.csv not found. Please run data_sim.py first.")
        return
    
    # Initialize detector
    detector = TouristAnomalyDetector()
    
    # Analyze data
    anomalies = detector.analyze_tourist_data(df, use_ml=True)
    
    print(f"\nDetected {len(anomalies)} anomalies:")
    for anomaly in anomalies:
        print(f"Tourist {anomaly['tourist_id']}: {anomaly['anomaly_type']} - {anomaly['details']}")
    
    # Test single point check
    print("\nTesting single point anomaly check...")
    test_anomaly = detector.check_single_point(
        tourist_id=999,
        lat=12.9800,  # Far from route
        lon=77.6000,
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    if test_anomaly:
        print(f"Single point test: {test_anomaly[0]['anomaly_type']} - {test_anomaly[0]['details']}")
    else:
        print("Single point test: No anomaly detected")

if __name__ == "__main__":
    main()
