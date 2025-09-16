# 🚀 Smart Tourist Safety - Integration Guide

## 📋 Overview
This guide explains how to set up and run all components of the Smart Tourist Safety system with AI anomaly detection.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Mobile App    │    │   Dashboard      │    │   AI Service    │
│   (React)       │    │   (React+TS)     │    │   (Python)      │
│   Port: 5173    │    │   Port: 5174     │    │   Port: 5001    │
└─────────┬───────┘    └────────┬─────────┘    └─────────┬───────┘
          │                     │                        │
          └─────────────────────┼────────────────────────┘
                                │
                    ┌───────────▼────────────┐
                    │     Backend API        │
                    │   (To be implemented)  │
                    │     Port: 5000         │
                    └────────────────────────┘
```

## 🔧 Component Setup

### 1. AI Service (Python Flask)
**Location:** `smart-tourist-safety/ai-service/`

```bash
# Navigate to AI service directory
cd smart-tourist-safety/ai-service

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate sample data
python data_sim.py

# Test anomaly detection
python anomaly.py

# Start AI service
python api.py
```

**Service will run on:** `http://localhost:5001`

**Available Endpoints:**
- `GET /health` - Health check
- `POST /check_anomaly` - Check single GPS point
- `POST /analyze_batch` - Analyze multiple GPS points
- `GET /stats` - Service statistics
- `GET /tourist_history/<id>` - Get tourist history

### 2. Dashboard (React + TypeScript)
**Location:** `smart-tourist-safety/dashboard/`

```bash
# Navigate to dashboard directory
cd smart-tourist-safety/dashboard

# Install dependencies
npm install

# Start development server
npm run dev
```

**Dashboard will run on:** `http://localhost:5174`

**Features:**
- Real-time tourist monitoring
- Interactive map with planned routes
- Alert panel for anomaly notifications
- Tourist list management

### 3. Mobile App (React)
**Location:** `smart-tourist-safety/mobile-app/`

```bash
# Navigate to mobile app directory
cd smart-tourist-safety/mobile-app

# Install dependencies
npm install

# Start development server
npm run dev
```

**Mobile app will run on:** `http://localhost:5173`

**Features:**
- Tourist registration
- GPS tracking with anomaly detection
- Emergency alert system
- Real-time safety status

## 🔗 Integration Points

### AI Service ↔ Mobile App
- **Endpoint:** `POST /check_anomaly`
- **Data Flow:** Mobile app sends GPS coordinates → AI service analyzes → Returns anomaly status
- **Frequency:** Real-time (every GPS update)

### AI Service ↔ Dashboard
- **Endpoint:** `GET /stats`
- **Data Flow:** Dashboard fetches statistics → AI service returns anomaly counts
- **Frequency:** Every 10 seconds

### Backend Integration (Pending)
The backend component will need to implement:

1. **Tourist Management:**
   ```
   GET /tourists - List all tourists
   POST /register - Register new tourist
   ```

2. **Location Tracking:**
   ```
   POST /location - Store tourist location
   GET /location/<id> - Get tourist location history
   ```

3. **Alert Management:**
   ```
   GET /alerts - Get active alerts
   POST /alerts - Create new alert
   ```

## 🚀 Quick Start (All Components)

### Terminal 1 - AI Service
```bash
cd smart-tourist-safety/ai-service
.\venv\Scripts\activate  # Windows
python api.py
```

### Terminal 2 - Dashboard
```bash
cd smart-tourist-safety/dashboard
npm run dev
```

### Terminal 3 - Mobile App
```bash
cd smart-tourist-safety/mobile-app
npm run dev
```

## 🧪 Testing the Integration

### 1. Test AI Service
```bash
curl -X POST http://localhost:5001/check_anomaly \
  -H "Content-Type: application/json" \
  -d '{"tourist_id":1,"lat":12.9716,"lon":77.5946,"timestamp":"2024-01-15T10:30:00"}'
```

### 2. Test Dashboard
- Open `http://localhost:5174`
- Check if tourist list loads
- Verify map displays with planned route
- Check alerts panel for anomaly notifications

### 3. Test Mobile App
- Open `http://localhost:5173`
- Register as a tourist
- Enable GPS tracking
- Move around to test anomaly detection

## 🔧 Configuration

### AI Service Configuration
**File:** `smart-tourist-safety/ai-service/anomaly.py`

```python
# Anomaly thresholds
stop_threshold_minutes = 5      # Minutes before stop is considered anomaly
deviation_threshold_meters = 200 # Meters from route before deviation anomaly

# Planned route coordinates
planned_route = [
    (12.9716, 77.5946),  # Start point
    (12.9726, 77.5956),  # Point 2
    (12.9736, 77.5966),  # Point 3
    (12.9746, 77.5976),  # Point 4
    (12.9756, 77.5986),  # End point
]
```

### Dashboard Configuration
**File:** `smart-tourist-safety/dashboard/src/components/TouristTable.tsx`

```typescript
// Backend API endpoint (update when backend is ready)
const res = await axios.get("http://<BACKEND_IP>:5000/tourists");
```

### Mobile App Configuration
**File:** `smart-tourist-safety/mobile-app/src/components/RegistrationForm.jsx`

```javascript
// Backend API endpoint (update when backend is ready)
const res = await axios.post('http://<BACKEND_IP>:5000/register', {
  // registration data
});
```

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**
   - AI service has CORS enabled for all origins
   - If issues persist, check browser console for specific errors

2. **GPS Not Working**
   - Ensure HTTPS is used in production
   - Check browser permissions for location access
   - Test on mobile device for better GPS accuracy

3. **AI Service Connection Failed**
   - Verify AI service is running on port 5001
   - Check if virtual environment is activated
   - Ensure all dependencies are installed

4. **Map Not Loading**
   - Check internet connection (maps require external tiles)
   - Verify Leaflet CSS is properly imported
   - Check browser console for JavaScript errors

### Port Conflicts
If ports are already in use:

- **AI Service:** Change port in `api.py` line: `app.run(host='0.0.0.0', port=5001)`
- **Dashboard:** Change port in `vite.config.ts`
- **Mobile App:** Change port in `vite.config.js`

## 📊 Data Flow Examples

### Normal Tourist Movement
```json
{
  "tourist_id": 1,
  "lat": 12.9716,
  "lon": 77.5946,
  "timestamp": "2024-01-15T10:30:00"
}
```
**AI Response:**
```json
{
  "status": "normal",
  "tourist_id": 1,
  "location": {"lat": 12.9716, "lon": 77.5946},
  "anomalies": []
}
```

### Anomaly Detection
```json
{
  "tourist_id": 1,
  "lat": 12.9800,  // Deviated from route
  "lon": 77.6000,
  "timestamp": "2024-01-15T10:35:00"
}
```
**AI Response:**
```json
{
  "status": "anomaly",
  "tourist_id": 1,
  "location": {"lat": 12.9800, "lon": 77.6000},
  "anomalies": [{
    "type": "route_deviation",
    "reason": "Deviated 512m from planned route",
    "confidence": 2.56
  }],
  "reason": "Deviated 512m from planned route"
}
```

## 🎯 Next Steps for Backend Integration

When your friend implements the backend, update these endpoints:

1. **Replace hardcoded backend IP** in dashboard and mobile app
2. **Implement real tourist data** instead of mock data
3. **Add authentication** if required
4. **Set up database** for persistent storage
5. **Add WebSocket** for real-time updates

## 📞 Support

For integration issues:
- Check this guide first
- Review browser console for errors
- Test each component individually
- Verify all services are running on correct ports

---

**🎉 Your Smart Tourist Safety system is ready for the hackathon!**
