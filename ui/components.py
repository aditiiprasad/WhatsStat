import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import helper
import pandas as pd

def render_sidebar():
    with st.sidebar:
        st.markdown("## 📁 Instructions")
        st.info("1. Open WhatsApp Chat\n2. More Options -> Export Chat\n3. Choose **'Without Media'**\n4. Upload the `.txt` file here")
        st.markdown("---")
        st.caption("🔒 Your data is processed locally in your browser/server instance and is not stored.")

def render_header():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #075E54; margin-bottom: 0;">📱 WhatsStat</h1>
        <p style="color: #666; font-size: 18px;">Advanced WhatsApp Chat Analyzer</p>
    </div>
    """, unsafe_allow_html=True)

def render_stats_section(selected_user, df):
    st.markdown("## 🔢 Top Statistics")
    num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Messages", f"{num_messages:,}")
    with col2:
        st.metric("Total Words", f"{words:,}")
    with col3:
        st.metric("Media Shared", f"{num_media:,}")
    with col4:
        st.metric("Links Shared", f"{num_links:,}")
        
    st.markdown("---")

def render_longest_message_section(df):
    user, message, length = helper.longest_message_sender(df)
    
    st.markdown("### 🏆 Longest Message Champion")
    st.markdown(f"""
    <div class="message-container">
        <div class="message-header">👤 {user} | 📏 {length} Characters</div>
        <div class="message-text">"{message[:500]}..."</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📖 Read Full Message"):
        st.write(message)

def render_most_active_users_section(selected_user, df):
    if selected_user == 'Overall':
        st.markdown("## 👑 Most Active Users")
        x, new_df = helper.most_busy_users(df)
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            fig = px.bar(
                x, x=x.index, y=x.values,
                labels={'x': 'User', 'y': 'Message Count'},
                color=x.values,
                color_continuous_scale='Greens'
            )
            fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("### 📊 User Breakdown")
            st.dataframe(new_df, hide_index=True, use_container_width=True)

def render_text_analysis_section(selected_user, df):
    st.markdown("## 🔤 Text Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ☁️ Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.imshow(df_wc)
        ax.axis('off')
        st.pyplot(fig)

    with col2:
        st.markdown("### 🗣️ Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        
        fig = px.bar(
            most_common_df,
            x='count',
            y='word',
            orientation='h',
            title="Top 20 Words",
            color='count',
            color_continuous_scale='Teal'
        )
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

def render_trending_topics_section(df):
    st.markdown("## 🔥 Trending Topics")
    topic_map = helper.trending_topics_by_month(df)
    
    if topic_map:
        months = list(topic_map.keys())
        selected_month = st.selectbox("Select Month to View Trends", months, index=len(months) - 1)
        
        if selected_month:
            topics = topic_map[selected_month]
            words_df = pd.DataFrame(list(topics.items()), columns=['Word', 'Count'])
            
            fig = px.bar(
                words_df,
                x='Word',
                y='Count',
                title=f"Trends in {selected_month}",
                color_discrete_sequence=['#25D366']
            )
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No trending data available.")

def render_conversation_starters_section(selected_user, df):
    st.markdown("## 🗣️ Conversation Drivers")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        starter_counts = helper.conversation_starters(df)
        fig = px.pie(
            values=starter_counts.values,
            names=starter_counts.index,
            title="Who starts conversations most often?",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Teal
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🌐 Languages")
        lang_df = helper.detect_languages(selected_user, df)
        st.dataframe(lang_df, use_container_width=True, hide_index=True)

def render_timeline_section(selected_user, df):
    st.markdown("## 📅 Activity Timeline")
    
    st.markdown("### Monthly Traffic")
    timeline = helper.monthly_timeline(selected_user, df)
    fig = px.line(
        timeline,
        x='time',
        y='message',
        markers=True,
        labels={'time': 'Month', 'message': 'Messages'},
        color_discrete_sequence=['#128C7E']
    )
    fig.update_layout(xaxis_tickangle=-45, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Daily Traffic")
    daily_timeline = helper.daily_timeline(selected_user, df)
    fig = px.line(
        daily_timeline,
        x='only_date',
        y='message',
        labels={'only_date': 'Date', 'message': 'Messages'},
        color_discrete_sequence=['#25D366']
    )
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

def render_activity_map_section(selected_user, df):
    st.markdown("## ⏰ Activity Habits")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Busiest Days")
        busy_day = helper.week_activity_map(selected_user, df)
        fig = px.bar(
            x=busy_day.index,
            y=busy_day.values,
            labels={'x': 'Day', 'y': 'Messages'},
            color_discrete_sequence=['#128C7E']
        )
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Busiest Months")
        busy_month = helper.month_activity_map(selected_user, df)
        fig = px.bar(
            x=busy_month.index,
            y=busy_month.values,
            labels={'x': 'Month', 'y': 'Messages'},
            color_discrete_sequence=['#25D366']
        )
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

def render_heatmaps_section(selected_user, df):
    st.markdown("## 🔥 Activity Heatmaps")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Weekly Schedule")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(user_heatmap, ax=ax, cmap="YlGnBu")
        st.pyplot(fig)

    with col2:
        st.markdown("### Hourly Habits")
        active_hour_heatmap = helper.most_active_hour_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(active_hour_heatmap, ax=ax, cmap="Greens")
        st.pyplot(fig)

def render_emoji_sentiment_section(selected_user, df):
    st.markdown("## 😄 Emotions & Emojis")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Top Emojis")
        emoji_df = helper.emoji_helper(selected_user, df)
        fig = px.pie(
            emoji_df.head(10),
            values='count',
            names='emoji',
            title='Top 10 Emojis',
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Sentiment Analysis")
        sentiments = helper.sentiment_analysis(selected_user, df)
        sentiment_df = pd.DataFrame(list(sentiments.items()), columns=['Sentiment', 'Count'])
        
        fig = px.bar(
            sentiment_df,
            x='Sentiment',
            y='Count',
            color='Sentiment',
            color_discrete_map={
                'positive': '#25D366',
                'negative': '#FF4B4B',
                'neutral': '#AAAAAA'
            }
        )
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

def render_analysis_sections(selected_user, df):
    render_longest_message_section(df)
    render_most_active_users_section(selected_user, df)
    render_text_analysis_section(selected_user, df)
    render_timeline_section(selected_user, df)
    render_activity_map_section(selected_user, df)
    render_heatmaps_section(selected_user, df)
    render_emoji_sentiment_section(selected_user, df)
    render_trending_topics_section(df)
    render_conversation_starters_section(selected_user, df)
