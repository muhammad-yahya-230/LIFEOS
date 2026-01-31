import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar():
    with st.sidebar:
        st.title("🧬 LifeOS")
        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "Planner", "Execution", "Gym", "Finance", "Knowledge", "Systems"],
            icons=["speedometer2", "calendar-check", "activity", "dumbbell", "wallet2", "journal-bookmark", "boxes"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#FAFAFA", "font-size": "14px"}, 
                "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#333"},
                "nav-link-selected": {"background-color": "#FF4B4B"},
            }
        )
    return selected

def render_card(label, value, delta=None, color=None):
    """Renders a custom styled metric card."""
    delta_html = ""
    if delta:
        color_hex = "#00FF00" if "inverse" not in str(color) else "#FF4B4B" # Simple logic
        delta_html = f"<span style='color: {color_hex}; font-size: 0.8rem; margin-left: 5px'>{delta}</span>"
        
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value} {delta_html}</div>
        </div>
    """, unsafe_allow_html=True)
