"""
Coin tracker module that combines Twitter tracking and sentiment analysis.
"""
from typing import Dict, List
from twitter_client import TwitterClient
from sentiment_analyzer import SentimentAnalyzer
import config


class CoinTracker:
    """Tracks meme coins and analyzes sentiment."""
    
    def __init__(self):
        """Initialize the coin tracker."""
        self.twitter_client = TwitterClient()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.tracked_coins = {}
    
    def add_coin(self, chat_id: int, coin_symbol: str, coin_name: str = None):
        """
        Add a coin to track for a specific chat.
        
        Args:
            chat_id: Telegram chat ID
            coin_symbol: Coin symbol (e.g., 'DOGE')
            coin_name: Optional coin name (e.g., 'Dogecoin')
        """
        if chat_id not in self.tracked_coins:
            self.tracked_coins[chat_id] = []
        
        coin_info = {
            'symbol': coin_symbol.upper(),
            'name': coin_name
        }
        
        # Check if coin is already tracked
        if not any(c['symbol'] == coin_info['symbol'] for c in self.tracked_coins[chat_id]):
            self.tracked_coins[chat_id].append(coin_info)
    
    def remove_coin(self, chat_id: int, coin_symbol: str) -> bool:
        """
        Remove a coin from tracking.
        
        Args:
            chat_id: Telegram chat ID
            coin_symbol: Coin symbol to remove
            
        Returns:
            True if coin was removed, False if not found
        """
        if chat_id not in self.tracked_coins:
            return False
        
        symbol_upper = coin_symbol.upper()
        initial_length = len(self.tracked_coins[chat_id])
        self.tracked_coins[chat_id] = [
            c for c in self.tracked_coins[chat_id] 
            if c['symbol'] != symbol_upper
        ]
        
        return len(self.tracked_coins[chat_id]) < initial_length
    
    def get_tracked_coins(self, chat_id: int) -> List[Dict]:
        """
        Get list of tracked coins for a chat.
        
        Args:
            chat_id: Telegram chat ID
            
        Returns:
            List of tracked coin dictionaries
        """
        return self.tracked_coins.get(chat_id, [])
    
    def analyze_coin(self, coin_symbol: str, coin_name: str = None) -> Dict:
        """
        Analyze sentiment for a specific coin.
        
        Args:
            coin_symbol: Coin symbol to analyze
            coin_name: Optional coin name
            
        Returns:
            Dictionary with tweets and sentiment analysis
        """
        # Build search query
        query = self.twitter_client.build_coin_query(coin_symbol, coin_name)
        
        # Get recent tweets
        tweets = self.twitter_client.search_recent_tweets(
            query, 
            max_results=config.MAX_TWEETS_PER_UPDATE
        )
        
        if not tweets:
            return {
                'symbol': coin_symbol.upper(),
                'name': coin_name,
                'tweets': [],
                'sentiment': None,
                'message': 'No recent tweets found'
            }
        
        # Analyze sentiment for each tweet
        sentiments = []
        for tweet in tweets:
            sentiment = self.sentiment_analyzer.analyze(tweet['text'])
            tweet['sentiment'] = sentiment
            sentiments.append(sentiment)
        
        # Aggregate sentiment
        aggregate = self.sentiment_analyzer.aggregate_sentiment(sentiments)
        
        return {
            'symbol': coin_symbol.upper(),
            'name': coin_name,
            'tweets': tweets,
            'sentiment': aggregate,
            'message': 'Analysis complete'
        }
    
    def format_analysis_message(self, analysis: Dict) -> str:
        """
        Format analysis results into a readable message.
        
        Args:
            analysis: Analysis dictionary from analyze_coin
            
        Returns:
            Formatted message string
        """
        symbol = analysis['symbol']
        name = analysis['name']
        sentiment = analysis['sentiment']
        tweets = analysis['tweets']
        
        if not sentiment:
            return f"No recent activity found for {symbol}"
        
        # Format header
        title = f"${symbol}"
        if name:
            title += f" ({name})"
        
        # Get sentiment emoji
        emoji = self.sentiment_analyzer.get_sentiment_emoji(sentiment['average_polarity'])
        category = self.sentiment_analyzer.categorize_sentiment(sentiment['average_polarity'])
        
        message = f"📊 *{title}* {emoji}\n\n"
        message += f"*Sentiment Analysis* ({sentiment['total_count']} tweets)\n"
        message += f"Overall: {category.upper()} ({sentiment['average_polarity']:.2f})\n\n"
        message += f"✅ Positive: {sentiment['positive_count']}\n"
        message += f"😐 Neutral: {sentiment['neutral_count']}\n"
        message += f"❌ Negative: {sentiment['negative_count']}\n\n"
        
        # Add top tweets
        message += "*Recent Tweets:*\n"
        for i, tweet in enumerate(tweets[:3], 1):
            text = tweet['text'][:100]
            if len(tweet['text']) > 100:
                text += "..."
            sentiment_emoji = self.sentiment_analyzer.get_sentiment_emoji(
                tweet['sentiment']['polarity']
            )
            message += f"{i}. {sentiment_emoji} {text}\n"
            message += f"   👤 @{tweet['author']['username']} "
            message += f"❤️ {tweet['metrics']['likes']} "
            message += f"🔄 {tweet['metrics']['retweets']}\n\n"
        
        return message
