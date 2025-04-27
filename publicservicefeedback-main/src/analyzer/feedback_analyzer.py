import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from typing import List, Dict
import pandas as pd
import re
import logging
from googletrans import Translator
from langdetect import detect, LangDetectException

class FeedbackAnalyzer:
    def __init__(self):
        nltk.download('vader_lexicon')
        self.sia = SentimentIntensityAnalyzer()
        self.translator = Translator()
        
        # Define supported Indian languages
        self.supported_languages = {
            'ta': 'Tamil',
            'hi': 'Hindi',
            'bn': 'Bengali',
            'te': 'Telugu',
            'gu': 'Gujarati',
            'mr': 'Marathi',
            'ml': 'Malayalam',
            'pa': 'Punjabi',
            'kn': 'Kannada',
            'or': 'Odia',
            'en': 'English'
        }
        
        self.negative_patterns = [
            r'(!{2,})',
            r'(\?!|\!\?){1,}',
            r'[!]{3,}'
        ]

    def detect_language(self, text: str) -> str:
        try:
            lang = detect(text)
            return lang if lang in self.supported_languages else 'en'
        except LangDetectException:
            return 'en'

    def translate_to_english(self, text: str, source_lang: str) -> str:
        if source_lang == 'en':
            return text
        try:
            translation = self.translator.translate(text, src=source_lang, dest='en')
            return translation.text
        except Exception as e:
            logging.error(f"Translation error: {str(e)}")
            return text

    def normalize_text(self, text: str) -> str:
        text = ' '.join(text.split())
        text = re.sub(r'[!]{2,}', '!', text)
        text = re.sub(r'[?]{2,}', '?', text)
        return text

    def get_emotion(self, sentiment: Dict) -> str:
        compound = sentiment['compound']
        pos = sentiment['pos']
        neg = sentiment['neg']
        
        if compound >= 0.3 and pos >= 0.3:
            return "Happy"
        elif compound <= -0.25 and neg >= 0.25:
            return "Angry"
        elif compound < 0 and neg > 0.15:
            return "Disappointed"
        elif compound > 0 and pos > 0.15:
            return "Satisfied"
        else:
            return "Neutral"
    
    def boost_sentiment_scores(self, text: str, sentiment: Dict) -> Dict:
        exclamation_count = text.count('!')
        repeated_punct = len(re.findall(r'[!?]{2,}', text))
        
        if exclamation_count > 0 or repeated_punct > 0:
            boost = min((exclamation_count + repeated_punct) * 0.1, 0.5)
            if sentiment['compound'] > 0:
                sentiment['pos'] += boost
            elif sentiment['compound'] < 0:
                sentiment['neg'] += boost
            
            sentiment['compound'] = sentiment['compound'] * (1 + boost)
        
        return sentiment
    
    def process_single_feedback(self, text: str, date: str = None) -> Dict:
        try:
            # Detect language
            original_lang = self.detect_language(text)
            original_text = text
            
            if original_lang != 'en':
                text = self.translate_to_english(text, original_lang)
            
            sentiment = self.sia.polarity_scores(text)
            sentiment = self.boost_sentiment_scores(text, sentiment)
            sentiment['compound'] = max(-1.0, min(1.0, sentiment['compound']))
            sentiment['emotion'] = self.get_emotion(sentiment)
            
            result = {
                'feedback': original_text,
                'translated_text': text if original_lang != 'en' else None,
                'original_lang': self.supported_languages.get(original_lang, original_lang),
                'emotion': sentiment['emotion'],
                'sentiment_score': sentiment['compound'],
                'positive': sentiment['pos'],
                'negative': sentiment['neg'],
                'neutral': sentiment['neu']
            }
            
            if date:
                result['date'] = date
                
            return result
        except Exception as e:
            logging.error(f"Error processing feedback: {str(e)}")
            return None

    def process_feedback(self, feedback_list: List[str], dates: List[str] = None) -> pd.DataFrame:
        results = []
        for i, feedback in enumerate(feedback_list):
            date = dates[i] if dates and i < len(dates) else None
            result = self.process_single_feedback(feedback, date)
            if result is not None:
                results.append(result)
        return pd.DataFrame(results)
    
    def analyze_file(self, filepath: str) -> pd.DataFrame:
        df = pd.read_csv(filepath)
        if 'feedback' in df.columns:
            dates = df['date'].tolist() if 'date' in df.columns else None
            return self.process_feedback(df['feedback'].tolist(), dates)
        return pd.DataFrame()