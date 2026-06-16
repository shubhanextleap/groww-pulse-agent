import streamlit as st
import json
import os
import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Groww Weekly Pulse",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed" # Hide sidebar for a cleaner "one-page" look
)

# --- Custom Styling (Groww Brand) ---
st.markdown("""
<style>
    /* Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Clean up the main header padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1000px; /* Keep the one-page note constrained */
    }
    
    /* Groww Green Accents */
    .groww-green {
        color: #00d09c;
    }
    
    .groww-bg {
        background-color: #00d09c;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    /* Theme Cards */
    .theme-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.2s ease;
    }
    .theme-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Quote Blocks */
    .user-quote {
        background: white;
        border-left: 4px solid #00d09c;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        font-style: italic;
        color: #334155;
    }
    
    /* Action Items */
    .action-item {
        display: flex;
        align-items: flex-start;
        background: #f0fdf4;
        border: 1px solid #dcfce7;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.75rem;
    }
    .action-icon {
        color: #16a34a;
        margin-right: 12px;
        font-size: 1.2rem;
    }
    .action-text {
        color: #166534;
        font-weight: 500;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #0f172a;
    }
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        color: #0f172a;
        display: flex;
        align-items: center;
        gap: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data(ttl=60)
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
    report_full = load_latest_report()
    
    if not report_full:
        st.info("👋 **Welcome to the Groww Pulse Dashboard!**\n\nThe AI Agent is currently crunching the machine learning models. Please wait a few minutes and refresh the page to see the latest report.")
        return

    # Extract JSON data
    report_data = report_full.get("report_data", {})
    iso_week = report_full.get("iso_week", "--")
    
    # Title Header
    st.markdown(f"<h1>Groww <span class='groww-green'>Weekly Pulse</span></h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='groww-bg'>Week: {iso_week}</div>", unsafe_allow_html=True)
    st.markdown("A highly scannable, one-page summary of what our users are saying right now across the App Store & Play Store.")
    st.markdown("---")

    # 1. Top Themes (Columns)
    st.markdown("<div class='section-title'>🎯 Top Themes</div>", unsafe_allow_html=True)
    themes = report_data.get("top_themes", [])
    if themes:
        cols = st.columns(len(themes))
        for i, theme in enumerate(themes):
            with cols[i]:
                st.markdown(f"""
                <div class='theme-card'>
                    <h3 style='margin-top:0; font-size: 1.1rem;'>{theme}</h3>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No themes extracted this week.")

    # 2. Real User Quotes
    st.markdown("<div class='section-title'>🗣️ What Users Are Saying</div>", unsafe_allow_html=True)
    quotes = report_data.get("user_quotes", [])
    if quotes:
        for quote in quotes:
            st.markdown(f"""
            <div class='user-quote'>
                "{quote}"
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No specific quotes highlighted.")

    # 3. Action Ideas
    st.markdown("<div class='section-title'>⚡ Actionable Ideas</div>", unsafe_allow_html=True)
    actions = report_data.get("action_ideas", [])
    if actions:
        for action in actions:
            st.markdown(f"""
            <div class='action-item'>
                <div class='action-icon'>✓</div>
                <div class='action-text'>{action}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No actions suggested.")
        
    st.markdown("---")
    st.caption("Generated autonomously. No PII included. For internal Product/Support/Leadership use only.")

if __name__ == "__main__":
    main()
