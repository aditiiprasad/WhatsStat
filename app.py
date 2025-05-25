import streamlit as st
import preprocessor
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import helper

st.set_page_config(layout='wide')

# CSS 
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# Additional CSS
st.markdown("""
<style>
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
</style>
""", unsafe_allow_html=True)

# Sidebar instructions
with st.sidebar:
    st.markdown("## 📁 Instructions")
    st.markdown("1. Export chat from WhatsApp **without media**")
    st.markdown("2. A `.zip` file will be created")
    st.markdown("3. Unzip it and upload the `.txt` file below")


# header 
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center;">
    <h1 style="margin: 0;">📱 WhatsStat</h1>
    <div style="text-align: right; font-size: 16px;">
        <p style="margin: 0;">👩‍💻 Developed by <strong>Aditi</strong></p>
        <a href="https://github.com/aditiiprasad" target="_blank" style="margin-right: 10px;"> GitHub</a>
        <a href="https://www.linkedin.com/in/aditiiprasad/" target="_blank"> LinkedIn</a>
    </div>
</div>
            
 ---           
""", unsafe_allow_html=True)


# Chat file upload
st.markdown("### Upload your chat file")
uploaded_file = st.file_uploader("Choose a WhatsApp chat file (.txt)", type="txt")

if uploaded_file is not None:
    # Decode and preprocess
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    # Chat selection and button
    selected_user = st.selectbox("🧐 Analyze chat for", user_list)

   
    st.markdown('<div class="button-row">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 4])
    
    with col1:
        analyze = st.button("✨ Show Analysis")
    
    # Initialize session state for analysis
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
    
    if analyze:
        st.session_state.analysis_done = True
    
    # reset button 
    if st.session_state.analysis_done:
        with col2:
            if st.button("🔄 Reset App"):
                st.session_state.analysis_done = False
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.analysis_done:
        # Stats
        st.markdown("## 🔢 Top Stats")
        num_messages, words, _, num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Messages", num_messages)
        with col2:
            st.metric("Total Words", words)
        with col3:
            st.metric("Links Shared", num_links)

        # Longest message sender
        st.markdown("## 📝 Longest Message Sender")
        user, message, length = helper.longest_message_sender(df)
        st.write(f"**{user}** sent the longest message ({length} characters):")
        
        # message display
        with st.expander("📖 View Longest Message", expanded=False):
            st.markdown(f"""
            <div class="message-container">
                <div class="message-header">
                    👤 From: <strong>{user}</strong> | 📏 Length: <strong>{length} characters</strong>
                </div>
                <div class="message-text">
                    {message}
              
            """, unsafe_allow_html=True)

        # Most active users 
        if selected_user == 'Overall':
            st.markdown("## 🧑‍🤝‍🧑 Most Active Users")
            x, new_df = helper.most_busy_users(df)
            col1, col2 = st.columns([1, 1])
            with col1:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.bar(x.index, x.values, color='#25D366')
                plt.xticks(rotation=45, fontsize=8)
                plt.yticks(fontsize=8)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            with col2:
                st.dataframe(new_df, use_container_width=True)

        # Word analysis section
        st.markdown("## 📊 Text Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ☁️ WordCloud")
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.imshow(df_wc)
            ax.axis('off')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        with col2:
            st.markdown("### 🔤 Most Common Words")
            most_common_df = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.barh(most_common_df['word'], most_common_df['count'], color='#128C7E')
            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)    

        # Trending topics
        st.markdown("## 🔥 Trending Topics by Month")
        topic_map = helper.trending_topics_by_month(df)
        
        if topic_map:
            # Get the latest month 
            months = list(topic_map.keys())
            latest_month = months[-1]
            
           
            st.markdown(f"### 📅 Latest: {latest_month}")
            latest_topics = topic_map[latest_month]
            words_df = pd.DataFrame(list(latest_topics.items()), columns=['Word', 'Count'])
            st.dataframe(words_df, use_container_width=True)
            
            # other months 
            if len(months) > 1:
                st.markdown("####  View Other Months:")
                other_months = months[:-1]  
                
                cols_per_row = 4
                for i in range(0, len(other_months), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, month in enumerate(other_months[i:i+cols_per_row]):
                        with cols[j]:
                            if st.button(f"📊 {month}", key=f"month_btn_{month}"):
                                st.markdown(f"##### Trending Topics for {month}")
                                month_topics = topic_map[month]
                                month_words_df = pd.DataFrame(list(month_topics.items()), columns=['Word', 'Count'])
                                st.dataframe(month_words_df, use_container_width=True)
        else:
            st.info("No trending topics data available.")

        # Conversation starters
        st.markdown("## 🗣️ Conversation Starters")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            starter_counts = helper.conversation_starters(df)
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(starter_counts.index, starter_counts.values, color='#128C7E')
            plt.xticks(rotation=45, fontsize=8)
            plt.yticks(fontsize=8)
            plt.title("Who starts chats most often?", fontsize=10)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        with col2:
            st.markdown("### 🌐 Languages Detected")
            lang_df = helper.detect_languages(selected_user, df)
            st.dataframe(lang_df, use_container_width=True)        


        # Timeline charts
        st.markdown("## 📅 Timeline Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(timeline['time'], timeline['message'], color='#25D366', linewidth=2)
            plt.xticks(rotation=45, fontsize=8)
            plt.yticks(fontsize=8)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        with col2:
            st.markdown("### Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#075E54', linewidth=2)
            plt.xticks(rotation=45, fontsize=8)
            plt.yticks(fontsize=8)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        # Activity map
        st.markdown("## 📊 Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("###  Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(5, 4))
            ax.bar(busy_day.index, busy_day.values, color='#128C7E')
            plt.xticks(rotation=45, fontsize=8)
            plt.yticks(fontsize=8)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        with col2:
            st.markdown("###  Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(5, 4))
            ax.bar(busy_month.index, busy_month.values, color='#25D366')
            plt.xticks(rotation=45, fontsize=8)
            plt.yticks(fontsize=8)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        # Heatmaps 
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##  Weekly Activity")
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.heatmap(user_heatmap, ax=ax, cmap="YlGnBu", cbar_kws={'shrink': 0.8})
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        with col2:
            st.markdown("##  Hourly Activity")
            active_hour_heatmap = helper.most_active_hour_heatmap(selected_user, df)
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.heatmap(active_hour_heatmap, cmap="coolwarm", ax=ax, cbar_kws={'shrink': 0.8})
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        

        # Emoji and Sentiment Analysis
        st.markdown("## 😄 Emoji & Sentiment Analysis")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Top Emojis")
            emoji_df = helper.emoji_helper(selected_user, df)
            st.dataframe(emoji_df.head(10), use_container_width=True)
            
        with col2:
            st.markdown("### Emoji Distribution")
            fig, ax = plt.subplots(figsize=(5, 4))
            ax.pie(emoji_df['count'].head(5), labels=emoji_df['emoji'].head(5), autopct="%0.1f%%")
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        with col3:
            st.markdown("### Sentiment Analysis")
            sentiments = helper.sentiment_analysis(selected_user, df)
            labels = list(sentiments.keys())
            values = list(sentiments.values())
            fig, ax = plt.subplots(figsize=(5, 4))
            ax.pie(values, labels=labels, autopct='%1.1f%%', colors=['#25D366', '#FF4B4B', '#AAAAAA'])
            ax.axis('equal')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)




# Footer
st.markdown("""
<hr style="margin-top: 50px; border: none; border-top: 2px solid #25D366;" />

<div style="text-align: center; padding: 20px 0; font-size: 14px; color: #555;">
    Developed with ❤️ by <strong>Aditi</strong> <br>
    <a href="https://github.com/aditiiprasad" target="_blank" style="text-decoration: none; color: #128C7E; font-weight: 600;">GitHub</a> |
    <a href="https://www.linkedin.com/in/aditiiprasad/" target="_blank" style="text-decoration: none; color: #128C7E; font-weight: 600;">LinkedIn</a>
</div>
""", unsafe_allow_html=True)

        