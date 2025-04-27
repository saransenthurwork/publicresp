from flask import Flask, render_template, request
import os
import sys
import pandas as pd
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analyzer.feedback_analyzer import FeedbackAnalyzer
from utils.text_preprocessor import preprocess_text

app = Flask(__name__)

def generate_suggestions(feedback, emotion, score):
    suggestions = []
    
    # Dictionary mapping feedback types to improvement suggestions
    improvement_map = {
        'wait_time': [
            "Implement digital queue management system",
            "Add more service counters during peak hours",
            "Enable online appointment booking",
            "Provide estimated wait times through SMS/app"
        ],
        'staff_behavior': [
            "Enhance staff training on customer service",
            "Implement regular feedback-based training sessions",
            "Develop standard operating procedures for common scenarios",
            "Introduce staff performance metrics based on feedback"
        ],
        'process': [
            "Streamline documentation requirements",
            "Digitize application processes",
            "Implement automated status updates",
            "Simplify forms and procedures"
        ],
        'communication': [
            "Improve multilingual support",
            "Set up clear communication channels",
            "Provide regular status updates",
            "Create detailed service guidelines"
        ],
        'infrastructure': [
            "Upgrade facility infrastructure",
            "Improve seating and waiting area comfort",
            "Enhance accessibility features",
            "Modernize service delivery systems"
        ]
    }
    
    # Simple keyword-based classification
    feedback_lower = feedback.lower()
    if any(word in feedback_lower for word in ['wait', 'long', 'queue', 'time']):
        suggestions.extend(improvement_map['wait_time'])
    if any(word in feedback_lower for word in ['rude', 'unhelpful', 'staff', 'officer', 'behavior']):
        suggestions.extend(improvement_map['staff_behavior'])
    if any(word in feedback_lower for word in ['process', 'procedure', 'system', 'documentation']):
        suggestions.extend(improvement_map['process'])
    if any(word in feedback_lower for word in ['communication', 'language', 'unclear', 'information']):
        suggestions.extend(improvement_map['communication'])
    if any(word in feedback_lower for word in ['facility', 'building', 'infrastructure', 'equipment']):
        suggestions.extend(improvement_map['infrastructure'])
    
    # If no specific category is detected, provide general suggestions
    if not suggestions:
        suggestions = [
            "Conduct detailed service quality assessment",
            "Implement regular staff training programs",
            "Set up automated feedback monitoring system",
            "Review and optimize service procedures"
        ]
    
    return suggestions[:3]  # Return top 3 most relevant suggestions

def calculate_statistics(results):
    total = len(results)
    
    # Group data by month for timeline
    timeline_data = {}
    for result in results:
        if 'date' in result:
            date = pd.to_datetime(result['date'])
            month_key = date.strftime('%Y-%m')
            if month_key not in timeline_data:
                timeline_data[month_key] = {'positive': 0, 'negative': 0, 'neutral': 0}
            
            if result['sentiment_score'] > 0:
                timeline_data[month_key]['positive'] += 1
            elif result['sentiment_score'] < 0:
                timeline_data[month_key]['negative'] += 1
                # Generate suggestions for negative feedback
                result['suggestions'] = generate_suggestions(
                    result['feedback'],
                    result['emotion'],
                    result['sentiment_score']
                )
            else:
                timeline_data[month_key]['neutral'] += 1

    stats = {
        'total': total,
        'positive_percent': len([r for r in results if r['sentiment_score'] > 0]) / total * 100,
        'negative_percent': len([r for r in results if r['sentiment_score'] < 0]) / total * 100,
        'neutral_percent': len([r for r in results if r['sentiment_score'] == 0]) / total * 100,
        'avg_sentiment': sum(r['sentiment_score'] for r in results) / total,
        'emotion_counts': {},
        'timeline_data': {
            'labels': sorted(timeline_data.keys()),
            'positive': [timeline_data[month]['positive'] for month in sorted(timeline_data.keys())],
            'negative': [timeline_data[month]['negative'] for month in sorted(timeline_data.keys())]
        }
    }
    
    for result in results:
        emotion = result['emotion']
        stats['emotion_counts'][emotion] = stats['emotion_counts'].get(emotion, 0) + 1
    
    return stats

def load_file_content(file):
    filename = file.filename.lower()
    temp_path = 'temp_upload'
    
    try:
        if filename.endswith('.csv'):
            file.save(temp_path + '.csv')
            return pd.read_csv(temp_path + '.csv')
        
        elif filename.endswith('.xlsx'):
            file.save(temp_path + '.xlsx')
            return pd.read_excel(temp_path + '.xlsx')
        
        elif filename.endswith('.json'):
            file.save(temp_path + '.json')
            with open(temp_path + '.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Convert JSON to DataFrame
            if isinstance(data, list):
                return pd.DataFrame(data)
            else:
                return pd.DataFrame([data])
        
        elif filename.endswith('.txt'):
            file.save(temp_path + '.txt')
            with open(temp_path + '.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()
            # Convert text lines to DataFrame
            return pd.DataFrame({'feedback': [line.strip() for line in lines if line.strip()]})
        
        else:
            raise ValueError("Unsupported file format")
            
    finally:
        # Cleanup temporary files
        for ext in ['.csv', '.xlsx', '.json', '.txt']:
            if os.path.exists(temp_path + ext):
                os.remove(temp_path + ext)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    analyzer = FeedbackAnalyzer()
    feedback_text = request.form.get('feedback_text', '').strip()
    
    if feedback_text:
        # Add current date for single feedback
        current_date = pd.Timestamp.now().strftime('%Y-%m-%d')
        preprocessed_feedback = [' '.join(preprocess_text(feedback_text))]
        results = analyzer.process_feedback(preprocessed_feedback, dates=[current_date])
        results_list = results.to_dict('records')
        stats = calculate_statistics(results_list)
        return render_template('index.html', results=results_list, stats=stats)
    
    elif 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No file selected")
        
        try:
            df = load_file_content(file)
            
            # Handle date column if present
            dates = None
            if 'date' in df.columns:
                dates = df['date'].tolist()
            
            # Check if feedback column exists
            if 'feedback' not in df.columns:
                df['feedback'] = df[df.columns[0]]
            
            preprocessed_feedback = [' '.join(preprocess_text(str(text))) for text in df['feedback']]
            results = analyzer.process_feedback(preprocessed_feedback, dates=dates)
            results_list = results.to_dict('records')
            stats = calculate_statistics(results_list)
            return render_template('index.html', results=results_list, stats=stats)
            
        except Exception as e:
            return render_template('index.html', error=f"Error processing file: {str(e)}")
    
    return render_template('index.html', error="Please enter feedback text or upload a file")

if __name__ == '__main__':
    app.run(debug=True)
