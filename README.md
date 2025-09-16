# 🛡️ Smart Tourist Safety System

An AI-powered tourist safety monitoring system with real-time anomaly detection, GPS tracking, and emergency response capabilities.

## 🎯 Project Overview

This system provides comprehensive safety monitoring for tourists using:
- **AI-powered anomaly detection** for unusual movement patterns
- **Real-time GPS tracking** with mobile app integration
- **Interactive dashboard** for monitoring multiple tourists
- **Emergency alert system** for immediate response

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

## 🚀 Quick Start

### Prerequisites
- **Python 3.7+** (for AI service)
- **Node.js 16+** (for frontend components)
- **Git** (for version control)

### 1. Clone Repository
```bash
git clone https://github.com/edwardtintu/smart-tourist-safety.git
cd smart-tourist-safety
```

### 2. Start AI Service
```bash
cd ai-service

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

# Start AI service
python api.py
```

### 3. Start Dashboard
```bash
# Open new terminal
cd dashboard

# Install dependencies
npm install

# Start dashboard
npm run dev
```

### 4. Start Mobile App
```bash
# Open new terminal
cd mobile-app

# Install dependencies
npm install

# Start mobile app
npm run dev
```

## 🧪 Testing

Run the integration test suite:
```bash
python test_integration.py
```

## 📱 Components

### AI Service (Port 5001)
- **Anomaly Detection**: Route deviation and stop detection
- **Machine Learning**: Isolation Forest for pattern analysis
- **REST API**: Real-time GPS analysis endpoints
- **Statistics**: System-wide safety metrics

### Dashboard (Port 5174)
- **Live Map**: Interactive tourist location tracking
- **Alert Panel**: Real-time anomaly notifications
- **Tourist Management**: Multi-tourist monitoring
- **Statistics Dashboard**: Safety analytics

### Mobile App (Port 5173)
- **GPS Tracking**: Continuous location monitoring
- **Safety Alerts**: Real-time anomaly notifications
- **Emergency Button**: One-click emergency alerts
- **Tourist Registration**: User onboarding system

## 🤖 AI Features

### Anomaly Detection Rules
- **Route Deviation**: Alerts when tourist moves >200m from planned route
- **Stop Detection**: Alerts when tourist stops >5 minutes
- **ML Pattern Analysis**: Detects unusual movement patterns using Isolation Forest

### Machine Learning
- **Algorithm**: Isolation Forest for unsupervised anomaly detection
- **Features**: Movement distance, time intervals, speed, location patterns
- **Training**: Automatic training on historical GPS data
- **Real-time**: Instant analysis of new GPS coordinates

## 📊 API Endpoints

### AI Service (localhost:5001)
- `GET /health` - Service health check
- `POST /check_anomaly` - Analyze single GPS point
- `POST /analyze_batch` - Analyze multiple GPS points
- `GET /stats` - System statistics
- `GET /tourist_history/<id>` - Tourist location history

### Example API Usage
```bash
# Check for anomalies
curl -X POST http://localhost:5001/check_anomaly \
  -H "Content-Type: application/json" \
  -d '{"tourist_id":1,"lat":12.9716,"lon":77.5946,"timestamp":"2024-01-15T10:30:00"}'

# Get system statistics
curl http://localhost:5001/stats
```

## 🔧 Configuration

### AI Service Settings
Edit `ai-service/anomaly.py`:
```python
# Anomaly thresholds
stop_threshold_minutes = 5      # Stop detection threshold
deviation_threshold_meters = 200 # Route deviation threshold

# Planned route coordinates
planned_route = [
    (12.9716, 77.5946),  # Start point
    (12.9726, 77.5956),  # Point 2
    # Add more coordinates...
]
```

## 🛠️ Development

### Project Structure
```
smart-tourist-safety/
├── ai-service/          # Python Flask AI service
│   ├── anomaly.py       # Anomaly detection logic
│   ├── api.py          # Flask REST API
│   ├── data_sim.py     # Data simulation
│   └── requirements.txt # Python dependencies
├── dashboard/           # React TypeScript dashboard
│   ├── src/components/  # React components
│   └── package.json    # Node.js dependencies
├── mobile-app/          # React mobile app
│   ├── src/components/  # React components
│   └── package.json    # Node.js dependencies
├── INTEGRATION_GUIDE.md # Detailed setup guide
└── test_integration.py  # Integration test suite
```

### Adding New Features
1. **AI Service**: Add new detection algorithms in `anomaly.py`
2. **Dashboard**: Create new components in `dashboard/src/components/`
3. **Mobile App**: Add features in `mobile-app/src/components/`

## 🚨 Emergency Features

### Mobile App Emergency System
- **One-click Emergency Button**: Instantly sends location and alert
- **Automatic Detection**: AI detects potential emergencies
- **Real-time Notifications**: Immediate alerts to monitoring dashboard

### Dashboard Emergency Response
- **Alert Prioritization**: Color-coded emergency levels
- **Location Tracking**: Real-time emergency location display
- **Response Coordination**: Integration ready for emergency services

## 📈 Monitoring & Analytics

### Real-time Statistics
- Total tourists tracked
- Active anomalies detected
- System performance metrics
- Historical trend analysis

### Safety Metrics
- Anomaly detection accuracy
- Response time analytics
- Tourist safety scores
- Route optimization insights

## 🔒 Security & Privacy

### Data Protection
- GPS data encrypted in transit
- No persistent storage of sensitive data
- Privacy-compliant location tracking
- Secure API endpoints with CORS protection

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **AI Service**: Advanced anomaly detection and machine learning
- **Dashboard**: Real-time monitoring and visualization
- **Mobile App**: GPS tracking and emergency response
- **Backend**: API integration and data management (in development)

## 🆘 Support

For setup issues or questions:
1. Check the [Integration Guide](INTEGRATION_GUIDE.md)
2. Run the test suite: `python test_integration.py`
3. Review component logs for error messages
4. Ensure all services are running on correct ports

---

**🎉 Ready for deployment and hackathon demonstration!**

Built with ❤️ for tourist safety and emergency response.
