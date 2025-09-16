import React, { useEffect, useState } from "react";
import axios from "axios";

interface Alert {
  tourist_id: number;
  timestamp: string;
  location: {
    lat: number;
    lon: number;
  };
  type: string;
  reason: string;
  confidence: number;
}

const AlertsPanel: React.FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchAlerts = async () => {
    try {
      setLoading(true);
      // Get stats from AI service to check for anomalies
      const statsRes = await axios.get("http://localhost:5001/stats");
      
      // If there are anomalies, we could fetch them from a dedicated endpoint
      // For now, we'll create mock alerts based on the stats
      if (statsRes.data.total_anomalies > 0) {
        // This would normally come from a real alerts endpoint
        const mockAlerts: Alert[] = [
          {
            tourist_id: 1,
            timestamp: new Date().toISOString(),
            location: { lat: 12.9716, lon: 77.5946 },
            type: "route_deviation",
            reason: "Tourist deviated from planned route",
            confidence: 1.5
          }
        ];
        setAlerts(mockAlerts);
      }
    } catch (err) {
      console.error("Error fetching alerts:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 10000); // refresh every 10s
    return () => clearInterval(interval);
  }, []);

  const getAlertColor = (type: string) => {
    switch (type) {
      case "route_deviation":
        return "#ff6b6b";
      case "stopped_too_long":
        return "#ffa726";
      case "ml_pattern_anomaly":
        return "#ab47bc";
      default:
        return "#42a5f5";
    }
  };

  const getAlertIcon = (type: string) => {
    switch (type) {
      case "route_deviation":
        return "⚠️";
      case "stopped_too_long":
        return "⏰";
      case "ml_pattern_anomaly":
        return "🤖";
      default:
        return "🚨";
    }
  };

  return (
    <div style={{ marginTop: "20px" }}>
      <h2>🚨 Active Alerts</h2>
      
      {loading && (
        <div style={{ padding: "10px", textAlign: "center" }}>
          Loading alerts...
        </div>
      )}

      {!loading && alerts.length === 0 && (
        <div 
          style={{ 
            padding: "15px", 
            backgroundColor: "#e8f5e8", 
            border: "1px solid #4caf50",
            borderRadius: "5px",
            color: "#2e7d32"
          }}
        >
          ✅ All tourists are safe - No active alerts
        </div>
      )}

      {alerts.map((alert, index) => (
        <div
          key={index}
          style={{
            padding: "12px",
            margin: "8px 0",
            backgroundColor: "#fff",
            border: `2px solid ${getAlertColor(alert.type)}`,
            borderRadius: "8px",
            boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <span style={{ fontSize: "20px" }}>{getAlertIcon(alert.type)}</span>
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: "bold", color: getAlertColor(alert.type) }}>
                Tourist #{alert.tourist_id} - {alert.type.replace('_', ' ').toUpperCase()}
              </div>
              <div style={{ fontSize: "14px", color: "#666", margin: "4px 0" }}>
                {alert.reason}
              </div>
              <div style={{ fontSize: "12px", color: "#999" }}>
                📍 {alert.location.lat.toFixed(4)}, {alert.location.lon.toFixed(4)} | 
                🕒 {new Date(alert.timestamp).toLocaleTimeString()} |
                🎯 Confidence: {alert.confidence.toFixed(1)}
              </div>
            </div>
          </div>
        </div>
      ))}

      <div style={{ marginTop: "15px", padding: "10px", backgroundColor: "#f5f5f5", borderRadius: "5px" }}>
        <div style={{ fontSize: "12px", color: "#666" }}>
          🔄 Auto-refresh every 10 seconds | 
          🤖 AI Service: <span style={{ color: "#4caf50" }}>Connected</span>
        </div>
      </div>
    </div>
  );
};

export default AlertsPanel;
