# helper/stats.py
from urlextract import URLExtract
import pandas as pd

extractor = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for msg in df['message']:
        words.extend(msg.split())

    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    links = []
    for msg in df['message']:
        links.extend(extractor.find_urls(msg))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    df_percent.columns = ['user', 'percent']
    return x, df_percent



def longest_message_sender(df):
    df['message_length'] = df['message'].apply(len)
    df_filtered = df[df['user'] != 'group_notification']
    longest_msg = df_filtered.loc[df_filtered['message_length'].idxmax()]
    return longest_msg['user'], longest_msg['message'], longest_msg['message_length']


def conversation_starter(df):
    df = df[df['user'] != 'group_notification']
    df['hour'] = df['date'].dt.hour
    early_df = df[df['hour'] < 7]  
    starter = early_df['user'].value_counts().idxmax()
    starter_count = early_df['user'].value_counts().max()
    return starter, starter_count


def conversation_starters(df, threshold_minutes=30):
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    df['gap'] = df['date'].diff().fillna(pd.Timedelta(seconds=0))
    df['new_convo'] = df['gap'] > pd.Timedelta(minutes=threshold_minutes)

    starters = df[df['new_convo']]['user']
    return starters.value_counts()
