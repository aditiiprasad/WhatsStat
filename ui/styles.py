# ui/styles.py
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
    /* Enhanced message container styling */
    .message-container {
        background: linear-gradient(135deg, #dcf8c6 0%, #b8e6b8 100%);
        border: 2px solid #25D366;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.2);
        font-family: 'Segoe UI', sans-serif;
        line-height: 1.5;
        word-wrap: break-word;
        position: relative;
    }

    .message-container::before {
        content: '💬';
        position: absolute;
        top: -10px;
        left: 15px;
        background: white;
        padding: 5px 10px;
        border-radius: 50%;
        font-size: 16px;
    }

    .message-text {
        color: #2c5530;
        font-size: 16px;
        font-weight: 500;
        margin-top: 10px;
    }

    .message-header {
        color: #075E54;
        font-weight: 700;
        font-size: 14px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Enhanced expander button styling */
    .stExpander > details > summary {
        background: linear-gradient(135deg, #25D366, #128C7E) !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        border: none !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(37, 211, 102, 0.3) !important;
    }

    .stExpander > details > summary:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.4) !important;
    }

    .stExpander > details[open] > summary {
        background: linear-gradient(135deg, #128C7E, #075E54) !important;
        border-radius: 25px 25px 0 0 !important;
    }

    /* Button row styling */
    .button-row {
        display: flex;
        gap: 15px;
        align-items: center;
        margin: 20px 0;
    }
    """

def apply_custom_css():
    """Apply all custom CSS styles"""
    # Load external CSS file
    load_css_file("style.css")
    
    # Apply additional custom CSS
    st.markdown(f"""
    <style>
    {get_custom_css()}
    </style>
    """, unsafe_allow_html=True)