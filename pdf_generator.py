from fpdf import FPDF
import pandas as pd

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'WhatsStat - Chat Analysis Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(selected_user, num_messages, words, num_media, num_links, most_busy_users, emoji_df, daily_timeline):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, f"Analysis Target: {selected_user}", ln=True, align='L')
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "1. General Statistics", ln=True)
    pdf.set_font("Arial", size=12)

    pdf.cell(50, 10, "Total Messages:", 0)
    pdf.cell(50, 10, str(num_messages), 1, 1)

    pdf.cell(50, 10, "Total Words:", 0)
    pdf.cell(50, 10, str(words), 1, 1)

    pdf.cell(50, 10, "Media Shared:", 0)
    pdf.cell(50, 10, str(num_media), 1, 1)

    pdf.cell(50, 10, "Links Shared:", 0)
    pdf.cell(50, 10, str(num_links), 1, 1)
    pdf.ln(10)

    if selected_user == 'Overall':
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, "2. Most Active Users (Top 5)", ln=True)
        pdf.set_font("Arial", size=12)

        top_users = most_busy_users[1].head(5)

        pdf.set_fill_color(200, 220, 255)
        pdf.cell(80, 10, "User", 1, 0, 'C', 1)
        pdf.cell(40, 10, "Percentage", 1, 1, 'C', 1)

        for index, row in top_users.iterrows():
            pdf.cell(80, 10, str(row['user']), 1)
            pdf.cell(40, 10, f"{row['percent']}%", 1, 1)
        pdf.ln(10)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "3. Top 5 Emojis Used", ln=True)
    pdf.set_font("Arial", 'B', 12)

    top_emojis = emoji_df.head(5)
    for index, row in top_emojis.iterrows():
        try:
            text = f"{row['emoji']} : {row['count']} times"
            pdf.cell(0, 10, text.encode('latin-1', 'replace').decode('latin-1'), ln=True)
        except:
            pdf.cell(0, 10, f"[Emoji] : {row['count']} times", ln=True)

    pdf.ln(10)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "4. Activity Peak", ln=True)
    pdf.set_font("Arial", size=12)

    peak_day = daily_timeline.sort_values('message', ascending=False).iloc[0]
    pdf.cell(0, 10, f"Highest Activity Date: {peak_day['only_date']}", ln=True)
    pdf.cell(0, 10, f"Messages on that day: {peak_day['message']}", ln=True)

    return pdf.output(dest='S').encode('latin-1')
