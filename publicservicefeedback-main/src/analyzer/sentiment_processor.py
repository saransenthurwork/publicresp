from typing import List, Dict
import pandas as pd

def process_sentiment_results(results: pd.DataFrame) -> Dict[str, float]:
    trends = {
        'average_sentiment': results['sentiment'].mean(),
        'positive_feedback_percentage': (results['sentiment'] > 0).mean() * 100,
        'negative_feedback_percentage': (results['sentiment'] < 0).mean() * 100,
        'neutral_feedback_percentage': (results['sentiment'] == 0).mean() * 100,
    }
    return trends

def analyze_sentiment_trends(feedback_data: List[str]) -> pd.DataFrame:
    return pd.DataFrame()