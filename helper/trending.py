# helper/trending.py
from collections import Counter

def trending_topics_by_month(df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read()

    df['month_year'] = df['date'].dt.to_period('M')
    df = df[df['message'] != '<Media omitted>']
    df = df[df['user'] != 'group_notification']

    result = {}

    for period, group in df.groupby('month_year'):
        words = []
        for msg in group['message']:
            for word in msg.lower().split():
                if word not in stop_words:
                    words.append(word)
        common = Counter(words).most_common(10)
        result[str(period)] = dict(common)

    return result
