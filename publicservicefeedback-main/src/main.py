import logging
from analyzer.feedback_analyzer import FeedbackAnalyzer
from data.data_loader import DataLoader
from utils.text_preprocessor import preprocess_text, download_nltk_resources
import sys
import os
import pandas as pd

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def initialize_nltk():
    try:
        download_nltk_resources()
    except Exception as e:
        print(f"Warning: NLTK initialization error: {e}")
        print("Proceeding with fallback methods...")

def display_results(analysis_results: pd.DataFrame):
    print("\n=== Feedback Analysis Results ===\n")
    
    for _, row in analysis_results.iterrows():
        print(f"Feedback: {row['feedback']}")
        print(f"Emotion: {row['emotion']}")
        print(f"Sentiment Score: {row['sentiment_score']:.2f}")
        print(f"Details: {row['positive']:.0%} Positive, {row['negative']:.0%} Negative, {row['neutral']:.0%} Neutral")
        print("-" * 80 + "\n")
    
    print("\n=== Analysis Summary ===")
    print(f"Total feedbacks analyzed: {len(analysis_results)}")
    print(f"Emotion distribution:\n{analysis_results['emotion'].value_counts()}")

def main():
    try:
        setup_logging()
        initialize_nltk()
        
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_file = os.path.join(current_dir, 'data', 'sample_feedback.csv')
        
        data_loader = DataLoader()
        feedback_data = data_loader.load_data(data_file, file_type='csv')

        if 'feedback' not in feedback_data.columns:
            logging.error("Input file must contain a 'feedback' column")
            sys.exit(1)

        preprocessed_feedback = [' '.join(preprocess_text(feedback)) for feedback in feedback_data['feedback']]

        analyzer = FeedbackAnalyzer()
        analysis_results = analyzer.process_feedback(preprocessed_feedback)

        display_results(analysis_results)

    except Exception as e:
        logging.error(f"Error during analysis: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()