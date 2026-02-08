# app.py
import streamlit as st
import preprocessor
import helper
from ui.components import render_header, render_sidebar, render_stats_section, render_analysis_sections
from ui.styles import apply_custom_css

# Page configuration
st.set_page_config(layout='wide', page_title="WhatsStat - WhatsApp Chat Analyzer")

# Apply custom CSS
apply_custom_css()

# Render sidebar
render_sidebar()

# Render header
render_header()

# Chat file upload
st.markdown("### Upload your chat file")
uploaded_file = st.file_uploader("Choose a WhatsApp chat file (.txt)", type="txt")

if uploaded_file is not None:
    # Decode and preprocess
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Get user list
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    # Chat selection
    selected_user = st.selectbox("🧐 Analyze chat for", user_list)

    # Control buttons
    st.markdown('<div class="button-row">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 4])
    
    with col1:
        analyze = st.button("✨ Show Analysis")
    
    # Initialize session state
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
    
    if analyze:
        st.session_state.analysis_done = True
    
    # Reset button
    if st.session_state.analysis_done:
        with col2:
            if st.button("🔄 Reset App"):
                st.session_state.analysis_done = False
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Show analysis if requested
    if st.session_state.analysis_done:
        # Render stats section
        render_stats_section(selected_user, df)
        
        # Render all analysis sections
        render_analysis_sections(selected_user, df)

# Footer
st.markdown("""
<hr style="margin-top: 50px; border: none; border-top: 2px solid #25D366;" />

<div style="text-align: center; padding: 20px 0; font-size: 14px; color: #555;">
    Developed with ❤️ by <strong>Aditi</strong> <br>
    <a href="https://github.com/aditiiprasad" target="_blank" style="text-decoration: none; color: #128C7E; font-weight: 600;">GitHub</a> |
    <a href="https://www.linkedin.com/in/aditiiprasad/" target="_blank" style="text-decoration: none; color: #128C7E; font-weight: 600;">LinkedIn</a>
</div>
""", unsafe_allow_html=True)