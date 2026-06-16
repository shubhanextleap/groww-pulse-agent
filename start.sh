#!/bin/bash
# Start the background scheduler job
python scheduler.py &

# If no data exists, run the agent in the background to instantly populate the dashboard!
if [ ! -f "data/latest_report.json" ]; then
    echo "No report found. Triggering initial generation..."
    python scheduler.py --test &
fi

# Start the Streamlit web dashboard
streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0
