import streamlit as st
import preprocessor
import helper
from ui.components import render_header, render_sidebar, render_stats_section, render_analysis_sections
from ui.styles import apply_custom_css
import pdf_generator

st.set_page_config(layout='wide', page_title="WhatsStat - WhatsApp Chat Analyzer")

apply_custom_css()

render_sidebar()

render_header()

st.markdown("### 📂 Upload your chat or Try Demo")

col1, col2 = st.columns([1, 1])

data = None

use_demo = st.checkbox("👉 Try with Demo Data (No upload needed)")

uploaded_file = st.file_uploader("Choose a WhatsApp chat file (.txt)", type="txt")

if use_demo:
    try:
        with open("sample_chat.txt", "r", encoding="utf-8") as f:
            data = f.read()
    except FileNotFoundError:
        st.error("Demo file 'sample_chat.txt' not found. Please upload a file.")

elif uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

if data is not None:
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    st.markdown("---")
    selected_user = st.selectbox("🧐 Analyze chat for", user_list)

    st.markdown('<div class="button-row">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 4])
    
    with col1:
        analyze = st.button("✨ Show Analysis")
    
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
    
    if analyze:
        st.session_state.analysis_done = True
    
    if st.session_state.analysis_done:
        with col2:
            if st.button("🔄 Reset App"):
                st.session_state.analysis_done = False
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.analysis_done:
        render_stats_section(selected_user, df)
        render_analysis_sections(selected_user, df)

        st.markdown("---")
        st.subheader("📥 Export Report")
        
        if st.button("📄 Generate PDF Report"):
            
            num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)
            most_busy_users = helper.most_busy_users(df)
            emoji_df = helper.emoji_helper(selected_user, df)
            daily_timeline = helper.daily_timeline(selected_user, df)
            
          
            pdf_bytes = pdf_generator.create_pdf(
                selected_user, num_messages, words, num_media, num_links, 
                most_busy_users, emoji_df, daily_timeline
            )
            
            
            st.download_button(
                label="⬇️ Download PDF Result",
                data=pdf_bytes,
                file_name=f"WhatsStat_Report_{selected_user}.pdf",
                mime="application/pdf"
            )
        

st.markdown("""
<hr style="margin-top: 50px; border: none; border-top: 2px solid #25D366;" />

<div style="text-align: center; padding: 20px 0; font-size: 14px; color: #555;">
    Developed with ❤️ by <strong>Aditi</strong> <br>
    <a href="https://github.com/aditiiprasad" target="_blank" style="text-decoration: none; color: #128C7E; font-weight: 600;">GitHub</a> |
    <a href="https://www.linkedin.com/in/aditiiprasad/" target="_blank" style="text-decoration: none; color: #128C7E; font-weight: 600;">LinkedIn</a>
</div>
""", unsafe_allow_html=True)
