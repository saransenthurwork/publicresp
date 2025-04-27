import unittest
from src.analyzer.feedback_analyzer import FeedbackAnalyzer

class TestFeedbackAnalyzer(unittest.TestCase):
    
    def setUp(self):
        self.analyzer = FeedbackAnalyzer()

    def test_analyze_text_positive(self):
        result = self.analyzer.analyze_text("I love the new public service!")
        self.assertGreater(result['compound'], 0)

    def test_analyze_text_negative(self):
        result = self.analyzer.analyze_text("The service was terrible and unhelpful.")
        self.assertLess(result['compound'], 0)

    def test_process_feedback(self):
        feedback_list = [
            "The new online portal is very user-friendly",
            "Wait times are too long at the service center",
            "Staff was helpful and professional"
        ]
        results = self.analyzer.process_feedback(feedback_list)
        self.assertEqual(len(results), len(feedback_list))
        self.assertIn('feedback', results.columns)
        self.assertIn('sentiment', results.columns)

if __name__ == '__main__':
    unittest.main()