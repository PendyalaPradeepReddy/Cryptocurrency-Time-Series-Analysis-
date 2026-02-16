"""
Run Script - Quick start for the crypto analytics dashboard
"""
import os
import sys
import subprocess

def main():
    # Get project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Add to path
    sys.path.insert(0, project_root)
    
    # Import config to create directories
    import config
    
    print("=" * 50)
    print("🚀 Crypto Analytics Dashboard")
    print("=" * 50)
    
    # Check if data exists
    data_exists = any(
        os.path.exists(os.path.join(config.PROCESSED_DATA_DIR, f"{coin}.csv"))
        for coin in config.CRYPTO_LIST.keys()
    )
    
    if not data_exists:
        print("\n📥 No data found. Fetching cryptocurrency data...")
        print("This may take a few minutes...\n")
        
        from src.data_collection import fetch_all_coins
        from src.preprocessing import preprocess_all_coins
        
        # Fetch data
        fetch_all_coins(days=config.DEFAULT_DAYS)
        
        # Preprocess
        preprocess_all_coins()
        
        print("\n✅ Data fetching complete!")
    else:
        print("\n✅ Data already exists. Skipping fetch.")
    
    print("\n🌐 Starting Streamlit dashboard...")
    print("Open your browser to: http://localhost:8501")
    print("\nPress Ctrl+C to stop the server.\n")
    
    # Run streamlit
    dashboard_path = os.path.join(project_root, "dashboard", "app.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", dashboard_path])


if __name__ == "__main__":
    main()
