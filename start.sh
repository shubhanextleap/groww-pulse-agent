#!/bin/bash
# Start the background scheduler job
python scheduler.py &

# Start the Streamlit web dashboard
streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0
