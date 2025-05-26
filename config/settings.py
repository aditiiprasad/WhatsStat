# Configuration settings for the WhatsApp analyzer

# App Configuration
APP_TITLE = "WhatsStat - WhatsApp Chat Analyzer"
LAYOUT = "wide"

# Developer Information
DEVELOPER_NAME = "Aditi"
GITHUB_URL = "https://github.com/aditiiprasad"
LINKEDIN_URL = "https://www.linkedin.com/in/aditiiprasad/"

# UI Colors (WhatsApp Theme)
COLORS = {
    'primary': '#25D366',      # WhatsApp green
    'secondary': '#128C7E',    # Dark green
    'tertiary': '#075E54',     # Darker green
    'background': '#dfecdd',   # Light green background
    'text': '#111b21',         # Dark text
    'negative': '#FF4B4B',     # Red for negative sentiment
    'neutral': '#AAAAAA'       # Gray for neutral sentiment
}

# Chart Configuration
CHART_CONFIG = {
    'figsize_default': (6, 4),
    'figsize_large': (8, 4),
    'figsize_small': (5, 4),
    'fontsize_small': 8,
    'fontsize_normal': 10,
    'fontsize_large': 12
}

# File Upload Configuration
UPLOAD_CONFIG = {
    'max_file_size': 200,  # MB
    'allowed_extensions': ['txt'],
    'encoding': 'utf-8'
}

# Analysis Configuration
ANALYSIS_CONFIG = {
    'max_common_words': 20,
    'max_emojis_display': 10,
    'max_trending_topics': 10,
    'cols_per_row': 4
}