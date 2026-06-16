import streamlit as st
import json
import os
import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Groww Weekly Pulse",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
# A clean, minimalistic style using Streamlit's native markdown injection
st.markdown("""
<style>
    /* Clean up the main header */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Make metrics pop slightly more */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #0F172A;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1rem;
        color: #64748B;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data(ttl=60) # Cache for 60 seconds so it picks up background updates
def load_latest_report():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    report_path = os.path.join(data_dir, "latest_report.json")
    
    if not os.path.exists(report_path):
        return None
        
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading report: {e}")
        return None

# --- Main App ---
def main():
    report_data = load_latest_report()
    
    # Sidebar
    with st.sidebar:
        st.title("Pulse Dashboard")
        st.markdown("Generated autonomously by **Antigravity AI**.")
        st.markdown("---")
        
        if report_data:
            st.metric("Current Product", report_data.get("product", "Unknown"))
            st.metric("ISO Week", report_data.get("iso_week", "--"))
            
            # Format timestamp safely
            try:
                dt = datetime.datetime.fromisoformat(report_data.get("timestamp", ""))
                formatted_time = dt.strftime("%B %d, %Y - %I:%M %p")
            except:
                formatted_time = report_data.get("timestamp", "Unknown")
                
            st.caption(f"**Last Updated:**\n{formatted_time}")
            
            st.markdown("---")
            st.success("System is Healthy")
            
        else:
            st.warning("Awaiting Data...")

    # Main Content Area
    if not report_data:
        st.info("👋 Welcome to the Groww Pulse Dashboard!\n\nThe AI Agent is currently crunching the machine learning models in the background. Please wait a few minutes and refresh the page to see the latest report.")
        return

    # Extract Content
    content = report_data.get("content", "")
    
    # Instead of showing the raw markdown `# Groww Weekly Pulse`, we can display it nicely
    st.markdown(content)

if __name__ == "__main__":
    main()
