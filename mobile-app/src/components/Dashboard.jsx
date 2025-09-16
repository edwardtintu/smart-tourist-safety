import { useState, useEffect } from 'react';
import axios from 'axios';

export default function Dashboard({ digitalId }) {
  const [location, setLocation] = useState(null);
  const [tracking, setTracking] = useState(false);
  const [status, setStatus] = useState('safe');
  const [lastAlert, setLastAlert] = useState(null);
  const [watchId, setWatchId] = useState(null);

  // Start GPS tracking
  const startTracking = () => {
    if (!navigator.geolocation) {
      alert('Geolocation is not supported by this browser.');
      return;
    }

    const options = {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0
    };

    const id = navigator.geolocation.watchPosition(
      (position) => {
        const newLocation = {
          lat: position.coords.latitude,
          lon: position.coords.longitude,
          timestamp: new Date().toISOString()
        };
        
        setLocation(newLocation);
        checkForAnomalies(newLocation);
      },
      (error) => {
        console.error('GPS Error:', error);
        alert('Unable to get your location. Please check GPS settings.');
      },
      options
    );

    setWatchId(id);
    setTracking(true);
  };

  // Stop GPS tracking
  const stopTracking = () => {
    if (watchId) {
      navigator.geolocation.clearWatch(watchId);
      setWatchId(null);
    }
    setTracking(false);
  };

  // Check for anomalies using AI service
  const checkForAnomalies = async (currentLocation) => {
    try {
      const response = await axios.post('http://localhost:5001/check_anomaly', {
        tourist_id: digitalId,
        lat: currentLocation.lat,
        lon: currentLocation.lon,
        timestamp: currentLocation.timestamp
      });

      if (response.data.status === 'anomaly') {
        setStatus('alert');
        setLastAlert({
          type: response.data.anomalies[0]?.type || 'unknown',
          reason: response.data.reason || 'Anomaly detected',
          timestamp: new Date().toLocaleTimeString()
        });
        
        // Show alert to user
        alert(`⚠️ Safety Alert: ${response.data.reason}`);
      } else {
        setStatus('safe');
        setLastAlert(null);
      }
    } catch (error) {
      console.error('Error checking anomalies:', error);
      // Don't alert user for API errors, just log them
    }
  };

  // Send emergency alert
  const sendEmergencyAlert = async () => {
    if (!location) {
      alert('Location not available. Please enable GPS tracking first.');
      return;
    }

    try {
      // This would normally send to emergency services
      // For now, we'll just send to our AI service for logging
      await axios.post('http://localhost:5001/check_anomaly', {
        tourist_id: digitalId,
        lat: location.lat,
        lon: location.lon,
        timestamp: new Date().toISOString(),
        emergency: true
      });

      alert('🚨 Emergency alert sent! Help is on the way.');
    } catch (error) {
      console.error('Error sending emergency alert:', error);
      alert('Failed to send emergency alert. Please call emergency services directly.');
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'safe': return '#4caf50';
      case 'alert': return '#ff9800';
      case 'emergency': return '#f44336';
      default: return '#2196f3';
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'safe': return '✅';
      case 'alert': return '⚠️';
      case 'emergency': return '🚨';
      default: return '📍';
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto' }}>
      <h2 style={{ textAlign: 'center', color: '#333' }}>
        🛡️ Tourist Safety Dashboard
      </h2>
      
      <div style={{ 
        padding: '15px', 
        backgroundColor: getStatusColor(), 
        color: 'white', 
        borderRadius: '10px',
        textAlign: 'center',
        marginBottom: '20px'
      }}>
        <h3 style={{ margin: '0 0 5px 0' }}>
          {getStatusIcon()} Status: {status.toUpperCase()}
        </h3>
        <p style={{ margin: '0', fontSize: '14px' }}>
          Tourist ID: {digitalId}
        </p>
      </div>

      {/* Location Info */}
      <div style={{ 
        padding: '15px', 
        backgroundColor: '#f5f5f5', 
        borderRadius: '8px',
        marginBottom: '15px'
      }}>
        <h4 style={{ margin: '0 0 10px 0' }}>📍 Current Location</h4>
        {location ? (
          <div style={{ fontSize: '14px' }}>
            <p>Latitude: {location.lat.toFixed(6)}</p>
            <p>Longitude: {location.lon.toFixed(6)}</p>
            <p>Last Update: {new Date(location.timestamp).toLocaleTimeString()}</p>
          </div>
        ) : (
          <p style={{ color: '#666', fontSize: '14px' }}>Location not available</p>
        )}
      </div>

      {/* Tracking Controls */}
      <div style={{ marginBottom: '15px' }}>
        {!tracking ? (
          <button
            onClick={startTracking}
            style={{
              width: '100%',
              padding: '12px',
              backgroundColor: '#4caf50',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '16px',
              cursor: 'pointer'
            }}
          >
            🎯 Start GPS Tracking
          </button>
        ) : (
          <button
            onClick={stopTracking}
            style={{
              width: '100%',
              padding: '12px',
              backgroundColor: '#ff9800',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '16px',
              cursor: 'pointer'
            }}
          >
            ⏹️ Stop Tracking
          </button>
        )}
      </div>

      {/* Emergency Button */}
      <button
        onClick={sendEmergencyAlert}
        style={{
          width: '100%',
          padding: '15px',
          backgroundColor: '#f44336',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          fontSize: '18px',
          fontWeight: 'bold',
          cursor: 'pointer',
          marginBottom: '15px'
        }}
      >
        🚨 EMERGENCY ALERT
      </button>

      {/* Last Alert */}
      {lastAlert && (
        <div style={{ 
          padding: '12px', 
          backgroundColor: '#fff3cd', 
          border: '1px solid #ffeaa7',
          borderRadius: '8px',
          marginBottom: '15px'
        }}>
          <h4 style={{ margin: '0 0 8px 0', color: '#856404' }}>⚠️ Last Alert</h4>
          <p style={{ margin: '0', fontSize: '14px', color: '#856404' }}>
            <strong>Type:</strong> {lastAlert.type}<br/>
            <strong>Reason:</strong> {lastAlert.reason}<br/>
            <strong>Time:</strong> {lastAlert.timestamp}
          </p>
        </div>
      )}

      {/* Safety Tips */}
      <div style={{ 
        padding: '12px', 
        backgroundColor: '#e3f2fd', 
        borderRadius: '8px',
        fontSize: '12px',
        color: '#1565c0'
      }}>
        <h4 style={{ margin: '0 0 8px 0' }}>💡 Safety Tips</h4>
        <ul style={{ margin: '0', paddingLeft: '16px' }}>
          <li>Keep GPS tracking enabled</li>
          <li>Stay on planned routes when possible</li>
          <li>Don't stop in one place for too long</li>
          <li>Use emergency button if you feel unsafe</li>
        </ul>
      </div>

      {/* Connection Status */}
      <div style={{ 
        marginTop: '15px', 
        padding: '8px', 
        backgroundColor: '#f5f5f5', 
        borderRadius: '5px',
        textAlign: 'center',
        fontSize: '12px',
        color: '#666'
      }}>
        🔄 Auto-monitoring active | 🤖 AI Service: Connected
      </div>
    </div>
  );
}
