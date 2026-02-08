# helper/langdetect_utils.py
from langdetect import detect, DetectorFactory
from collections import Counter
import pandas as pd
from language_utils import get_language_name

DetectorFactory.seed = 0

def detect_languages(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>')]
    temp = temp[temp['message'].str.len() > 20]  # skip very short messages

    # Sample messages if large dataset
    sample_size = 1000
    if len(temp) > sample_size:
        temp = temp.sample(n=sample_size, random_state=42)

    lang_cache = {}
    languages = []
    for msg in temp['message']:
        if msg in lang_cache:
            lang = lang_cache[msg]
        else:
            try:
                lang = detect(msg)
            except:
                lang = None
            lang_cache[msg] = lang
        if lang:
            languages.append(lang)

    lang_counts = Counter(languages)
    lang_df = pd.DataFrame(lang_counts.most_common(3), columns=['Language', 'Count'])
    lang_df['Language'] = lang_df['Language'].apply(get_language_name)

    return lang_df
