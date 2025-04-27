import pandas as pd
import matplotlib.pyplot as plt
import re
from matplotlib import gridspec

# Read the CSV file
df = pd.read_csv('../data/sample_feedback.csv')

# Function to detect language
def detect_language(text):
    if re.search('[\u0900-\u097F]', text):  # Hindi
        return 'Hindi'
    elif re.search('[\u0B80-\u0BFF]', text):  # Tamil
        return 'Tamil'
    return 'English'

# Function to detect emotion
def detect_emotion(text):
    text = text.lower()
    if any(word in text for word in ['excellent', 'good', 'satisfied', 'appreciate', 'helpful', 'courteous']):
        return 'Positive'
    elif any(word in text for word in ['poor', 'terrible', 'bad', 'worst', 'unacceptable', 'disappointed']):
        return 'Negative'
    return 'Neutral'

# Define professional color palette
COLORS = {
    'language': ['#4e79a7', '#f28e2c', '#59a14f'],  # Blue, Orange, Green
    'emotion': {
        'positive': '#4e79a7',    # Professional blue
        'negative': '#e15759',    # Muted red
        'neutral': '#76b7b2'      # Teal
    },
    'timeline': ['#4e79a7', '#e15759', '#76b7b2']  # Blue, Red, Teal
}

# Set style and figure properties
plt.style.use('seaborn')
fig = plt.figure(figsize=(15, 4.5), facecolor='white')  # Reduced from (20, 6)
fig.patch.set_alpha(1.0)

# Create gridspec with proper spacing
gs = gridspec.GridSpec(1, 3, width_ratios=[1, 1, 1.2], wspace=0.2)

# Language Distribution (Left subplot)
ax1 = plt.subplot(gs[0])
ax1.set_facecolor('white')
language_dist = df['feedback'].apply(detect_language).value_counts()
wedges, texts, autotexts = ax1.pie(language_dist, labels=language_dist.index, 
                                  autopct='%1.1f%%', 
                                  colors=COLORS['language'],
                                  textprops={'fontsize': 10})
ax1.set_title('Language Distribution in Feedback', pad=15, fontsize=11)  # Reduced padding and font size

# Center the pie chart
plt.setp(autotexts, size=8)  # Reduced from 9
plt.setp(texts, size=9)      # Reduced from 10

# Emotion Bar Chart (Middle subplot)
ax2 = plt.subplot(gs[1])
ax2.set_facecolor('white')
emotion_dist = df['feedback'].apply(detect_emotion).value_counts()
bars = ax2.bar(emotion_dist.index, emotion_dist.values, 
               color=[COLORS['emotion'][x.lower()] for x in emotion_dist.index],
               width=0.6)  # Adjust bar width
ax2.set_title('Overall Emotion Distribution', pad=15, fontsize=11)
ax2.set_ylabel('Number of Feedbacks', fontsize=9)
ax2.tick_params(axis='both', labelsize=8)

# Add value labels on bars with adjusted position
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}\n({height/len(df)*100:.1f}%)',
             ha='center', va='bottom',
             fontsize=8)  # Reduced from 9

# Emotion Timeline (Right subplot)
ax3 = plt.subplot(gs[2])
ax3.set_facecolor('white')
df['date'] = pd.to_datetime(df['date'])
df['emotion'] = df['feedback'].apply(detect_emotion)

# Group by date and emotion, count occurrences
timeline_data = df.groupby(['date', 'emotion']).size().unstack(fill_value=0)

# Plot stacked area chart with improved styling
timeline_data.plot(kind='area', stacked=True, 
                  color=COLORS['timeline'],
                  alpha=0.8, ax=ax3)
ax3.set_title('Emotion Distribution Over Time', pad=15, fontsize=11)
ax3.set_xlabel('Date', fontsize=9)
ax3.set_ylabel('Number of Feedbacks', fontsize=9)
ax3.tick_params(axis='both', labelsize=8)
ax3.legend(title='Emotion', bbox_to_anchor=(1.02, 1), fontsize=8, title_fontsize=9)

# Adjust overall layout with specific padding and margins
plt.tight_layout(pad=1.5, w_pad=2.0, h_pad=1.0)  # Reduced padding values

# Save with improved settings
plt.savefig('../output/distribution_analysis.png', 
            bbox_inches='tight', 
            dpi=300,
            facecolor='white',
            edgecolor='none',
            pad_inches=0.5)
plt.close()

# Print summary
print("\nAnalysis Summary:")
print("Language Distribution:", dict(language_dist))
print("Emotion Distribution:", dict(emotion_dist))
