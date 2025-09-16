#!/usr/bin/env python3
"""
Integration Test Script for Smart Tourist Safety System
Tests all AI service endpoints and verifies functionality
"""

import requests
import json
import time
from datetime import datetime

# Configuration
AI_SERVICE_URL = "http://localhost:5001"
TEST_TOURIST_ID = 999

def test_health_check():
    """Test AI service health endpoint"""
    print("🔍 Testing AI Service Health Check...")
    try:
        response = requests.get(f"{AI_SERVICE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['status']} - {data['service']}")
            return True
        else:
            print(f"❌ Health Check Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health Check Error: {e}")
        return False

def test_normal_location():
    """Test normal GPS location (should not trigger anomaly)"""
    print("\n🎯 Testing Normal Location...")
    try:
        payload = {
            "tourist_id": TEST_TOURIST_ID,
            "lat": 12.9716,  # On planned route
            "lon": 77.5946,
            "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        }
        
        response = requests.post(f"{AI_SERVICE_URL}/check_anomaly", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Normal Location: Status = {data['status']}")
            print(f"   📍 Location: {data['location']['lat']}, {data['location']['lon']}")
            return data['status'] == 'normal'
        else:
            print(f"❌ Normal Location Test Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Normal Location Error: {e}")
        return False

def test_route_deviation():
    """Test route deviation anomaly"""
    print("\n⚠️ Testing Route Deviation Anomaly...")
    try:
        payload = {
            "tourist_id": TEST_TOURIST_ID,
            "lat": 12.9800,  # Far from planned route
            "lon": 77.6000,
            "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        }
        
        response = requests.post(f"{AI_SERVICE_URL}/check_anomaly", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Route Deviation: Status = {data['status']}")
            if data['status'] == 'anomaly':
                print(f"   🚨 Anomaly Type: {data['anomalies'][0]['type']}")
                print(f"   📝 Reason: {data['reason']}")
                print(f"   🎯 Confidence: {data['anomalies'][0]['confidence']}")
            return data['status'] == 'anomaly'
        else:
            print(f"❌ Route Deviation Test Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Route Deviation Error: {e}")
        return False

def test_batch_analysis():
    """Test batch analysis endpoint"""
    print("\n📊 Testing Batch Analysis...")
    try:
        payload = {
            "data": [
                {
                    "tourist_id": TEST_TOURIST_ID,
                    "lat": 12.9716,
                    "lon": 77.5946,
                    "timestamp": "2024-01-15T10:30:00"
                },
                {
                    "tourist_id": TEST_TOURIST_ID,
                    "lat": 12.9800,  # Deviation
                    "lon": 77.6000,
                    "timestamp": "2024-01-15T10:35:00"
                }
            ]
        }
        
        response = requests.post(f"{AI_SERVICE_URL}/analyze_batch", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Batch Analysis: {data['total_points']} points analyzed")
            print(f"   🚨 Anomalies Detected: {data['anomalies_detected']}")
            return data['anomalies_detected'] > 0
        else:
            print(f"❌ Batch Analysis Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Batch Analysis Error: {e}")
        return False

def test_statistics():
    """Test statistics endpoint"""
    print("\n📈 Testing Statistics...")
    try:
        response = requests.get(f"{AI_SERVICE_URL}/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Statistics Retrieved:")
            print(f"   👥 Total Tourists: {data['total_tourists']}")
            print(f"   📍 Total Data Points: {data['total_data_points']}")
            print(f"   🚨 Total Anomalies: {data['total_anomalies']}")
            print(f"   📊 Anomaly Rate: {data['anomaly_rate']}%")
            return True
        else:
            print(f"❌ Statistics Test Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Statistics Error: {e}")
        return False

def test_tourist_history():
    """Test tourist history endpoint"""
    print("\n📚 Testing Tourist History...")
    try:
        response = requests.get(f"{AI_SERVICE_URL}/tourist_history/{TEST_TOURIST_ID}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Tourist History Retrieved:")
            print(f"   👤 Tourist ID: {data['tourist_id']}")
            print(f"   📍 Total Points: {data['total_points']}")
            return True
        elif response.status_code == 404:
            print(f"✅ Tourist History: No history found (expected for new tourist)")
            return True
        else:
            print(f"❌ Tourist History Test Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Tourist History Error: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 Smart Tourist Safety - Integration Test Suite")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Normal Location", test_normal_location),
        ("Route Deviation", test_route_deviation),
        ("Batch Analysis", test_batch_analysis),
        ("Statistics", test_statistics),
        ("Tourist History", test_tourist_history)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            time.sleep(1)  # Small delay between tests
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
    
    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your AI service is ready for integration!")
        print("\n📋 Next Steps:")
        print("1. Start the dashboard: cd smart-tourist-safety/dashboard && npm run dev")
        print("2. Start the mobile app: cd smart-tourist-safety/mobile-app && npm run dev")
        print("3. Test the complete system integration")
    else:
        print("⚠️ Some tests failed. Please check the AI service setup.")
        print("💡 Make sure the AI service is running on http://localhost:5001")
    
    print("\n🔗 Integration Guide: smart-tourist-safety/INTEGRATION_GUIDE.md")

if __name__ == "__main__":
    main()
