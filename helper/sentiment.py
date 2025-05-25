from textblob import TextBlob

def sentiment_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df = df[df['message'] != '<Media omitted>']
    df = df[df['user'] != 'group_notification']

    sentiments = {'positive': 0, 'negative': 0, 'neutral': 0}

    for msg in df['message']:
        analysis = TextBlob(msg)
        polarity = analysis.sentiment.polarity
        if polarity > 0:
            sentiments['positive'] += 1
        elif polarity < 0:
            sentiments['negative'] += 1
        else:
            sentiments['neutral'] += 1

    return sentiments
