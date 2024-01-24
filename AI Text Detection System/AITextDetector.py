import os
import re
import string
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import language_tool_python

# Download NLTK resources (run this once)
import nltk
nltk.download('vader_lexicon')

# Load the dataset with negative and positive words
dataset_filename = 'Positive and Negative Word List.xlsx'
dataset_path = os.path.join(os.path.dirname(__file__), dataset_filename)
df = pd.read_excel(dataset_path)

# Create a mapping dictionary from negative to positive words
word_mapping = dict(zip(df['Negative Sense Word List'], df['Positive Sense Word List']))

# Initialize Sentiment Intensity Analyzer
sia = SentimentIntensityAnalyzer()

# Initialize LanguageTool
tool = language_tool_python.LanguageTool('en-US')

# Function to detect and correct bad language
def detect_and_correct_bad_language(text):
    # Analyze sentiment
    sentiment_score = sia.polarity_scores(text)['compound']

    # If sentiment is negative, replace negative words
    if sentiment_score < 0:
        words = text.split()
        for i, word in enumerate(words):
            if word in word_mapping:
                words[i] = word_mapping[word]

        # Join the words back into a sentence
        corrected_text = ' '.join(words)
        return corrected_text
    else:
        return text

# Function to check grammar and coherence
def check_grammar(text):
    matches = tool.check(text)
    if matches:
        # If there are grammar issues, suggest corrections
        return language_tool_python.utils.correct(text, matches)
    else:
        return text

# Main function to filter text
def filter_text(input_text):
    # Remove emojis
    input_text = ''.join(c for c in input_text if c <= '\uFFFF')

    # Detect and correct bad language based on sentiment
    filtered_text = detect_and_correct_bad_language(input_text)

    # Check grammar and coherence
    final_text = check_grammar(filtered_text)

    return {
        'filtered_text': final_text
    }

# Example usage
user_input = "You are an idiot"
result = filter_text(user_input)
print(result)
