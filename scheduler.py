import schedule
import time
import subprocess
import os

def run_pipeline():
    print(f"--- Scheduler: Starting Weekly Pipeline at {time.ctime()} ---")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Regenerate cache
    print("Scheduler: Running data ingestion (regenerate_cache.py)...")
    cache_cmd = ["python", os.path.join(script_dir, "scripts", "regenerate_cache.py")]
    cache_proc = subprocess.run(cache_cmd, capture_output=True, text=True)
    if cache_proc.returncode != 0:
        print(f"Scheduler: Data ingestion failed:\n{cache_proc.stderr}")
        return
        
    print("Scheduler: Data ingestion completed.")
    
    # 2. Run main agent
    print("Scheduler: Running main agent pipeline (main.py)...")
    main_cmd = ["python", os.path.join(script_dir, "main.py")]
    main_proc = subprocess.run(main_cmd, capture_output=True, text=True)
    if main_proc.returncode != 0:
        print(f"Scheduler: Main agent failed:\n{main_proc.stderr}")
        return
        
    print(f"--- Scheduler: Weekly Pipeline Completed at {time.ctime()} ---")

# Schedule for every Monday at 09:00 IST (Assuming the machine's timezone is IST)
schedule.every().monday.at("09:00").do(run_pipeline)

if __name__ == "__main__":
    print("Scheduler started. Waiting for next scheduled run (Monday 09:00).")
    print("Press Ctrl+C to exit.")
    
    # Run once immediately for testing if --test is provided
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Test mode enabled. Running immediately...")
        run_pipeline()
    
    while True:
        schedule.run_pending()
        time.sleep(60) # check every minute
