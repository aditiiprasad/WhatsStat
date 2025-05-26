import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import helper

def render_sidebar():
    """Render sidebar with instructions"""
    with st.sidebar:
        st.markdown("## 📁 Instructions")
        st.markdown("1. Export chat from WhatsApp **without media**")
        st.markdown("2. A `.zip` file will be created")
        st.markdown("3. Unzip it and upload the `.txt` file below")

def render_header():
    """Render main header"""
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

def render_stats_section(selected_user, df):
    """Render top statistics section"""
    st.markdown("## 🔢 Top Stats")
    num_messages, words, _, num_links = helper.fetch_stats(selected_user, df)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Messages", num_messages)
    with col2:
        st.metric("Total Words", words)
    with col3:
        st.metric("Links Shared", num_links)

def render_longest_message_section(df):
    """Render longest message section"""
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

def render_most_active_users_section(selected_user, df):
    """Render most active users section"""
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

def render_text_analysis_section(selected_user, df):
    """Render word analysis section"""
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

def render_trending_topics_section(df):
    """Render trending topics section"""
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

def render_conversation_starters_section(selected_user, df):
    """Render conversation starters and language detection section"""
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

def render_timeline_section(selected_user, df):
    """Render timeline analysis section"""
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

def render_activity_map_section(selected_user, df):
    """Render activity map section"""
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

def render_heatmaps_section(selected_user, df):
    """Render heatmaps section"""
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

def render_emoji_sentiment_section(selected_user, df):
    """Render emoji and sentiment analysis section"""
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

def render_analysis_sections(selected_user, df):
    """Render all analysis sections"""
    render_longest_message_section(df)
    render_most_active_users_section(selected_user, df)
    render_text_analysis_section(selected_user, df)
    render_trending_topics_section(df)
    render_conversation_starters_section(selected_user, df)
    render_timeline_section(selected_user, df)
    render_activity_map_section(selected_user, df)
    render_heatmaps_section(selected_user, df)
    render_emoji_sentiment_section(selected_user, df)