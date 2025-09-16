"""
Tourist Data Simulation Module
Generates mock GPS data for testing anomaly detection
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import math

class TouristDataSimulator:
    def __init__(self):
        # Base route coordinates (example: tourist route in a city)
        self.base_route = [
            (12.9716, 77.5946),  # Start point
            (12.9726, 77.5956),  # Point 2
            (12.9736, 77.5966),  # Point 3
            (12.9746, 77.5976),  # Point 4
            (12.9756, 77.5986),  # End point
        ]
        
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
    
    def generate_normal_movement(self, tourist_id, start_time, duration_minutes=60):
        """Generate normal tourist movement data"""
        data = []
        current_time = start_time
        
        # Generate points along the route
        for i in range(len(self.base_route) - 1):
            start_point = self.base_route[i]
            end_point = self.base_route[i + 1]
            
            # Generate intermediate points
            num_points = random.randint(8, 12)
            for j in range(num_points):
                progress = j / (num_points - 1)
                
                # Interpolate between start and end points
                lat = start_point[0] + (end_point[0] - start_point[0]) * progress
                lon = start_point[1] + (end_point[1] - start_point[1]) * progress
                
                # Add small random variation (normal GPS noise)
                lat += random.uniform(-0.0001, 0.0001)
                lon += random.uniform(-0.0001, 0.0001)
                
                data.append({
                    'tourist_id': tourist_id,
                    'lat': lat,
                    'lon': lon,
                    'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'is_anomaly': False,
                    'anomaly_type': 'normal'
                })
                
                # Increment time (normal walking pace: 1-2 minutes between points)
                current_time += timedelta(minutes=random.uniform(1, 2))
        
        return data
    
    def generate_stop_anomaly(self, tourist_id, start_time):
        """Generate data showing tourist stopped for too long"""
        data = []
        current_time = start_time
        
        # Normal movement first
        lat, lon = self.base_route[1]  # Stop at second point
        
        # Add normal points leading to stop
        for i in range(3):
            data.append({
                'tourist_id': tourist_id,
                'lat': lat + random.uniform(-0.0001, 0.0001),
                'lon': lon + random.uniform(-0.0001, 0.0001),
                'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                'is_anomaly': False,
                'anomaly_type': 'normal'
            })
            current_time += timedelta(minutes=1)
        
        # Generate stopped points (same location for 8 minutes)
        stop_duration = 8  # minutes (exceeds 5-minute threshold)
        for i in range(stop_duration):
            data.append({
                'tourist_id': tourist_id,
                'lat': lat + random.uniform(-0.00005, 0.00005),  # Very small variation
                'lon': lon + random.uniform(-0.00005, 0.00005),
                'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                'is_anomaly': True,
                'anomaly_type': 'stopped_too_long'
            })
            current_time += timedelta(minutes=1)
        
        return data
    
    def generate_deviation_anomaly(self, tourist_id, start_time):
        """Generate data showing tourist deviated from route"""
        data = []
        current_time = start_time
        
        # Start normally
        lat, lon = self.base_route[2]  # Start from third point
        
        # Add normal point
        data.append({
            'tourist_id': tourist_id,
            'lat': lat,
            'lon': lon,
            'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_anomaly': False,
            'anomaly_type': 'normal'
        })
        current_time += timedelta(minutes=1)
        
        # Generate deviation (move 300m away from route)
        deviation_distance = 0.003  # Approximately 300m in degrees
        deviated_lat = lat + deviation_distance
        deviated_lon = lon + deviation_distance
        
        for i in range(5):
            data.append({
                'tourist_id': tourist_id,
                'lat': deviated_lat + random.uniform(-0.0001, 0.0001),
                'lon': deviated_lon + random.uniform(-0.0001, 0.0001),
                'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                'is_anomaly': True,
                'anomaly_type': 'route_deviation'
            })
            current_time += timedelta(minutes=1)
        
        return data
    
    def generate_complete_dataset(self):
        """Generate complete dataset with normal and anomalous data"""
        all_data = []
        base_time = datetime.now() - timedelta(hours=2)
        
        # Generate normal tourist data
        normal_data = self.generate_normal_movement(1, base_time)
        all_data.extend(normal_data)
        
        # Generate stop anomaly
        stop_data = self.generate_stop_anomaly(2, base_time + timedelta(minutes=30))
        all_data.extend(stop_data)
        
        # Generate deviation anomaly
        deviation_data = self.generate_deviation_anomaly(3, base_time + timedelta(hours=1))
        all_data.extend(deviation_data)
        
        return pd.DataFrame(all_data)

def main():
    """Generate and save tourist data"""
    print("Generating tourist simulation data...")
    
    simulator = TouristDataSimulator()
    df = simulator.generate_complete_dataset()
    
    # Save to CSV
    df.to_csv('tourist_data.csv', index=False)
    
    print(f"Generated {len(df)} data points")
    print(f"Normal points: {len(df[df['is_anomaly'] == False])}")
    print(f"Anomaly points: {len(df[df['is_anomaly'] == True])}")
    print("Data saved to tourist_data.csv")
    
    # Display sample data
    print("\nSample data:")
    print(df.head(10))

if __name__ == "__main__":
    main()
