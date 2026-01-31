import streamlit as st
from config import THEME_COLOR

def apply_custom_styles():
    st.markdown(f"""
        <style>
            /* Main Background and Text */
            .stApp {{
                background-color: #0E1117;
                color: #FAFAFA;
            }}
            
            /* Sidebar */
            [data-testid="stSidebar"] {{
                background-color: #262730;
                border-right: 1px solid #333;
            }}
            
            /* Card Component */
            .metric-card {{
                background-color: #1E1E1E;
                padding: 15px;
                border-radius: 10px;
                border: 1px solid #333;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                margin-bottom: 10px;
            }}
            .metric-label {{
                font-size: 0.8rem;
                color: #AAAAAA;
                margin-bottom: 5px;
            }}
            .metric-value {{
                font-size: 1.5rem;
                font-weight: bold;
                color: #FFFFFF;
            }}
            
            /* Headers */
            h1, h2, h3 {{
                color: #FFFFFF !important;
                font-family: 'Inter', sans-serif;
            }}
            
            /* Inputs */
            .stTextInput>div>div>input {{
                background-color: #262730;
                color: white;
                border: 1px solid #444;
            }}
            
            /* Buttons */
            .stButton>button {{
                background-color: {THEME_COLOR};
                color: white;
                border: none;
                border-radius: 5px;
                transition: all 0.3s ease;
            }}
            .stButton>button:hover {{
                box-shadow: 0 0 10px {THEME_COLOR};
                border: 1px solid white;
            }}
        </style>
    """, unsafe_allow_html=True)
