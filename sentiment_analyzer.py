"""
Sentiment analysis module for analyzing tweet sentiment.
Uses TextBlob for simple and effective sentiment analysis.
"""
from textblob import TextBlob
from typing import Dict, List


class SentimentAnalyzer:
    """Analyzes sentiment of text using TextBlob."""
    
    def __init__(self):
        """Initialize the sentiment analyzer."""
        pass
    
    def analyze(self, text: str) -> Dict[str, float]:
        """
        Analyze the sentiment of a given text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary with polarity (-1 to 1) and subjectivity (0 to 1)
        """
        blob = TextBlob(text)
        return {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
    
    def categorize_sentiment(self, polarity: float) -> str:
        """
        Categorize sentiment based on polarity score.
        
        Args:
            polarity: Polarity score from -1 to 1
            
        Returns:
            Sentiment category: 'positive', 'negative', or 'neutral'
        """
        if polarity > 0.1:
            return 'positive'
        elif polarity < -0.1:
            return 'negative'
        else:
            return 'neutral'
    
    def get_sentiment_emoji(self, polarity: float) -> str:
        """
        Get an emoji representation of sentiment.
        
        Args:
            polarity: Polarity score from -1 to 1
            
        Returns:
            Emoji representing the sentiment
        """
        if polarity > 0.5:
            return '🚀'
        elif polarity > 0.1:
            return '😊'
        elif polarity < -0.5:
            return '📉'
        elif polarity < -0.1:
            return '😟'
        else:
            return '😐'
    
    def aggregate_sentiment(self, sentiments: List[Dict[str, float]]) -> Dict[str, any]:
        """
        Aggregate multiple sentiment scores.
        
        Args:
            sentiments: List of sentiment dictionaries
            
        Returns:
            Aggregated sentiment statistics
        """
        if not sentiments:
            return {
                'average_polarity': 0,
                'average_subjectivity': 0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'total_count': 0
            }
        
        polarities = [s['polarity'] for s in sentiments]
        subjectivities = [s['subjectivity'] for s in sentiments]
        
        positive_count = sum(1 for p in polarities if p > 0.1)
        negative_count = sum(1 for p in polarities if p < -0.1)
        neutral_count = len(polarities) - positive_count - negative_count
        
        return {
            'average_polarity': sum(polarities) / len(polarities),
            'average_subjectivity': sum(subjectivities) / len(subjectivities),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'total_count': len(sentiments)
        }
