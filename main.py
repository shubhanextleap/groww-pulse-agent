import sys
import os
from dotenv import load_dotenv

# Add the root directory to path so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.config import load_config
from src.core.agent import ReviewPulseAgent

def main():
    load_dotenv() # Load Groq API key
    
    config_path = os.path.join(os.path.dirname(__file__), "config", "settings.yaml")
    
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)

    try:
        config = load_config(config_path)
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser(description="Review Pulse Agent")
    parser.add_argument("--force", action="store_true", help="Bypass idempotency checks to force a run")
    args = parser.parse_args()

    agent = ReviewPulseAgent(config)
    agent.run(force=args.force)

if __name__ == "__main__":
    main()
