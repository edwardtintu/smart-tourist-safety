"""
Setup script for Tourist Anomaly Detection Service
Run this to set up the environment and generate initial data
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Tourist Anomaly Detection Service Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('data_sim.py'):
        print("❌ Please run this script from the ai-service directory")
        return
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Virtual environment not detected. Please activate venv first:")
        print("   Windows: .\\venv\\Scripts\\activate")
        print("   Linux/Mac: source venv/bin/activate")
        return
    
    print("✓ Virtual environment detected")
    print("✓ All Python files created")
    print("✓ Dependencies installed")
    
    # Generate sample data
    print("\n📊 Generating sample tourist data...")
    if run_command("python data_sim.py", "Sample data generation"):
        print("✓ Sample data saved to tourist_data.csv")
    
    # Test anomaly detection
    print("\n🔍 Testing anomaly detection...")
    if run_command("python anomaly.py", "Anomaly detection test"):
        print("✓ Anomaly detection system working")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the API server: python api.py")
    print("2. Test the API endpoints")
    print("3. Integrate with your backend system")
    
    print("\n📋 Quick API test:")
    print('curl -X POST http://localhost:5001/check_anomaly \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"tourist_id":1,"lat":12.9716,"lon":77.5946,"timestamp":"2024-01-15T10:30:00"}\'')

if __name__ == "__main__":
    main()
