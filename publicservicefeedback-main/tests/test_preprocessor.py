import unittest
from src.utils.text_preprocessor import tokenize, lemmatize, remove_stopwords

class TestTextPreprocessor(unittest.TestCase):
    def test_tokenize(self):
        text = "The quick brown fox jumps over the lazy dog."
        expected_output = ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]
        self.assertEqual(tokenize(text), expected_output)

    def test_lemmatize(self):
        words = ["running", "ran", "better"]
        expected_output = ["run", "ran", "better"]
        self.assertEqual(lemmatize(words), expected_output)

    def test_remove_stopwords(self):
        text = "This is a sample sentence with stopwords."
        stopwords = ["is", "a", "with"]
        expected_output = "This sample sentence stopwords."
        self.assertEqual(remove_stopwords(text, stopwords), expected_output)

if __name__ == '__main__':
    unittest.main()