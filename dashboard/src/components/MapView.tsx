import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// Fix for default markers in react-leaflet
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

interface TouristLocation {
  tourist_id: number;
  lat: number;
  lon: number;
  timestamp: string;
  is_anomaly: boolean;
  anomaly_type: string;
}

const MapVisualization: React.FC = () => {
  const [touristLocations, setTouristLocations] = useState<TouristLocation[]>([]);
  const [loading, setLoading] = useState(false);

  // Planned route coordinates (same as in AI service)
  const plannedRoute = [
    [12.9716, 77.5946],
    [12.9726, 77.5956],
    [12.9736, 77.5966],
    [12.9746, 77.5976],
    [12.9756, 77.5986],
  ];

  const fetchTouristLocations = async () => {
    try {
      setLoading(true);
      // Get stats from AI service
      const statsRes = await axios.get("http://localhost:5001/stats");
      
      // For demo purposes, create mock locations based on the planned route
      // In a real app, this would come from the backend with actual tourist locations
      const mockLocations: TouristLocation[] = [
        {
          tourist_id: 1,
          lat: 12.9716,
          lon: 77.5946,
          timestamp: new Date().toISOString(),
          is_anomaly: false,
          anomaly_type: "normal"
        },
        {
          tourist_id: 2,
          lat: 12.9726,
          lon: 77.5956,
          timestamp: new Date().toISOString(),
          is_anomaly: false,
          anomaly_type: "normal"
        },
        {
          tourist_id: 3,
          lat: 12.9800, // Deviated location
          lon: 77.6000,
          timestamp: new Date().toISOString(),
          is_anomaly: true,
          anomaly_type: "route_deviation"
        }
      ];
      
      setTouristLocations(mockLocations);
    } catch (err) {
      console.error("Error fetching tourist locations:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTouristLocations();
    const interval = setInterval(fetchTouristLocations, 15000); // refresh every 15s
    return () => clearInterval(interval);
  }, []);

  const getMarkerColor = (isAnomaly: boolean, anomalyType: string) => {
    if (!isAnomaly) return "green";
    
    switch (anomalyType) {
      case "route_deviation":
        return "red";
      case "stopped_too_long":
        return "orange";
      case "ml_pattern_anomaly":
        return "purple";
      default:
        return "blue";
    }
  };

  const createCustomIcon = (color: string) => {
    return L.divIcon({
      className: 'custom-div-icon',
      html: `<div style="
        background-color: ${color};
        width: 20px;
        height: 20px;
        border-radius: 50%;
        border: 3px solid white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
      "></div>`,
      iconSize: [20, 20],
      iconAnchor: [10, 10]
    });
  };

  const getStatusEmoji = (isAnomaly: boolean, anomalyType: string) => {
    if (!isAnomaly) return "✅";
    
    switch (anomalyType) {
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
    <div>
      <h2>🗺️ Tourist Location Map</h2>
      
      {loading && (
        <div style={{ padding: "10px", textAlign: "center" }}>
          Loading map data...
        </div>
      )}

      <div style={{ height: "500px", width: "100%", border: "2px solid #ddd", borderRadius: "8px" }}>
        <MapContainer
          center={[12.9736, 77.5966]}
          zoom={15}
          style={{ height: "100%", width: "100%" }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          
          {/* Planned Route */}
          <Polyline
            positions={plannedRoute as [number, number][]}
            color="blue"
            weight={4}
            opacity={0.7}
            dashArray="10, 10"
          />
          
          {/* Tourist Markers */}
          {touristLocations.map((location) => (
            <Marker
              key={location.tourist_id}
              position={[location.lat, location.lon]}
              icon={createCustomIcon(getMarkerColor(location.is_anomaly, location.anomaly_type))}
            >
              <Popup>
                <div style={{ minWidth: "200px" }}>
                  <h3 style={{ margin: "0 0 8px 0" }}>
                    {getStatusEmoji(location.is_anomaly, location.anomaly_type)} Tourist #{location.tourist_id}
                  </h3>
                  <p><strong>Status:</strong> {location.is_anomaly ? "⚠️ ANOMALY" : "✅ Normal"}</p>
                  {location.is_anomaly && (
                    <p><strong>Type:</strong> {location.anomaly_type.replace('_', ' ')}</p>
                  )}
                  <p><strong>Location:</strong> {location.lat.toFixed(4)}, {location.lon.toFixed(4)}</p>
                  <p><strong>Last Update:</strong> {new Date(location.timestamp).toLocaleTimeString()}</p>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>

      <div style={{ marginTop: "10px", padding: "10px", backgroundColor: "#f5f5f5", borderRadius: "5px" }}>
        <div style={{ display: "flex", gap: "20px", fontSize: "12px", color: "#666" }}>
          <div>🔵 Planned Route</div>
          <div>🟢 Normal Tourist</div>
          <div>🔴 Route Deviation</div>
          <div>🟠 Stopped Too Long</div>
          <div>🟣 ML Anomaly</div>
        </div>
        <div style={{ marginTop: "5px", fontSize: "12px", color: "#666" }}>
          🔄 Auto-refresh every 15 seconds | 📍 {touristLocations.length} tourists tracked
        </div>
      </div>
    </div>
  );
};

export default MapVisualization;
