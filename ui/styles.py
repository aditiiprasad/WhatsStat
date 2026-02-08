import streamlit as st

def load_css_file(file_path):
    """Load CSS from external file"""
    try:
        with open(file_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file {file_path} not found. Using default styles.")

def get_custom_css():
    """Return custom CSS as string"""
    return """
    /* Main container styling */
    .main {
        background-color: #f0f2f5;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
        transition: transform 0.2s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* Headers */
    h1, h2, h3 {
        color: #128C7E;
        font-weight: 600;
    }

    /* Custom Message Box */
    .message-container {
        background: linear-gradient(135deg, #dcf8c6 0%, #ffffff 100%);
        border-left: 5px solid #25D366;
        border-radius: 8px;
        padding: 15px 20px;
        margin: 15px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        font-family: 'Segoe UI', sans-serif;
        color: #303030;
    }

    .message-header {
        font-size: 0.85rem;
        color: #075E54;
        margin-bottom: 8px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .message-text {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #111b21;
    }

    /* Button Styling */
    .stButton > button {
        background-color: #128C7E;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s;
    }

    .stButton > button:hover {
        background-color: #075E54;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    /* Hide Streamlit default menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    """

def apply_custom_css():
    """Apply all custom CSS styles"""
    st.markdown(f"""
    <style>
    {get_custom_css()}
    </style>
    """, unsafe_allow_html=True)