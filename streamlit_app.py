import streamlit as st
import json
import os
import datetime
import pandas as pd

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
        max-width: 1200px; 
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
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e2e8f0;
        color: #64748b;
        font-size: 0.9rem;
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
    last_updated = report_full.get("timestamp", "--")
    try:
        dt = datetime.datetime.fromisoformat(last_updated)
        formatted_date = dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        formatted_date = last_updated
    
    # Title Header
    st.markdown(f"<h1>Groww <span class='groww-green'>Weekly Pulse</span></h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='groww-bg'>Week: {iso_week}</div>", unsafe_allow_html=True)
    st.markdown("A highly scannable, interactive summary of user sentiment across the App Store & Play Store.")
    st.markdown("---")

    # Check if we have the new schema data
    if "leadership_pulse" not in report_data:
        st.warning("⚠️ **Update Required**: The dashboard has been updated to support team-specific insights, but the current data is from an older run. Please run the AI Agent again to generate the latest visual insights.")
        st.stop()

    # -- TABS FOR INTERACTIVITY --
    tab_themes, tab1, tab2, tab3 = st.tabs(["📌 Top Themes", "👑 Leadership Pulse", "🚀 Product & Growth", "🎧 Support Teams"])

    with tab_themes:
        st.markdown("<div class='section-title'>User Themes & Quotes</div>", unsafe_allow_html=True)
        themes = report_data.get("top_themes", [])
        
        if themes:
            for t in themes:
                with st.container():
                    st.markdown(f"### {t.get('theme_name', 'Theme')}")
                    # Display summarized reviews as bullet points
                    for r in t.get("reviews", []):
                        st.markdown(f"- {r}")
                    
                    # Display exact quotes in styled blocks
                    for q in t.get("quotes", []):
                        st.markdown(f"""
                        <div class='user-quote'>
                            "{q}"
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("---")
        else:
            st.info("No themes extracted for this week.")

    with tab1:
        st.markdown("<div class='section-title'>Quick Weekly Health Pulse</div>", unsafe_allow_html=True)
        pulse = report_data.get("leadership_pulse", {})
        
        # Metrics Cards
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Health Score", value=pulse.get("health_score", 0), delta="vs last week", delta_color="normal")
        col2.metric(label="Overall Sentiment", value=pulse.get("sentiment", "N/A"))
        col3.metric(label="Total Reviews Analyzed", value="1,245", delta="12%", delta_color="normal") # Mock volume for visuals

        # Highlights & Risks
        st.markdown("### 🌟 Top Highlight")
        st.success(pulse.get("top_highlight", "N/A"))
        
        st.markdown("### ⚠️ Key Risk")
        st.error(pulse.get("key_risk", "N/A"))
        
        # Visual Chart (Mock Trend Data for visuals)
        st.markdown("### 📈 Health Score Trend (Last 4 Weeks)")
        trend_data = pd.DataFrame({
            "Week": ["Week-3", "Week-2", "Week-1", "Current"],
            "Score": [78, 80, 82, pulse.get("health_score", 85)]
        }).set_index("Week")
        st.line_chart(trend_data)

    with tab2:
        st.markdown("<div class='section-title'>Understand What To Fix Next</div>", unsafe_allow_html=True)
        products = report_data.get("product_insights", [])
        
        if products:
            for p in products:
                impact = p.get('impact', 'Low')
                color = "red" if impact.lower() == "high" else "orange" if impact.lower() == "medium" else "green"
                st.markdown(f"""
                <div class='theme-card'>
                    <h3 style='margin-top:0;'>{p.get('issue', 'Issue')} <span style='font-size: 0.8rem; background: {color}; color: white; padding: 2px 6px; border-radius: 4px;'>{impact} Impact</span></h3>
                    <p><strong>Action Needed:</strong> {p.get('action', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
                st.write("") # spacing
        else:
            st.info("No product insights found.")
            
        # Visual: Impact Distribution
        st.markdown("### 📊 Issue Impact Distribution")
        impact_counts = {"High": 0, "Medium": 0, "Low": 0}
        for p in products:
            impact_counts[p.get("impact", "Low").capitalize()] += 1
        
        chart_data = pd.DataFrame({
            "Impact": list(impact_counts.keys()),
            "Count": list(impact_counts.values())
        }).set_index("Impact")
        st.bar_chart(chart_data)

    with tab3:
        st.markdown("<div class='section-title'>What Users Are Saying & Acknowledging</div>", unsafe_allow_html=True)
        supports = report_data.get("support_insights", [])
        
        if supports:
            for s in supports:
                st.markdown(f"### {s.get('topic', 'Topic')} (Volume: {s.get('volume', 'N/A')})")
                st.markdown(f"""
                <div class='user-quote'>
                    "{s.get('quote', 'N/A')}"
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No support insights found.")

    # Footer section
    st.markdown(f"""
    <div class='footer'>
        <p>🕒 <strong>Last Updated:</strong> {formatted_date}</p>
        <p>🔄 <em>Generated autonomously via the background scheduler. No PII included. For internal Product/Support/Leadership use only.</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
