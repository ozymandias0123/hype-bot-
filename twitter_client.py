"""
Twitter/X client for tracking tweets about meme coins.
"""
import tweepy
import logging
from typing import List, Dict
import config

# Set up logging
logger = logging.getLogger(__name__)


class TwitterClient:
    """Client for interacting with Twitter/X API."""
    
    def __init__(self):
        """Initialize Twitter client with API credentials."""
        self.client = tweepy.Client(
            bearer_token=config.TWITTER_BEARER_TOKEN,
            consumer_key=config.TWITTER_API_KEY,
            consumer_secret=config.TWITTER_API_SECRET,
            access_token=config.TWITTER_ACCESS_TOKEN,
            access_token_secret=config.TWITTER_ACCESS_SECRET,
            wait_on_rate_limit=True
        )
    
    def search_recent_tweets(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search for recent tweets matching the query.
        
        Args:
            query: Search query for tweets
            max_results: Maximum number of tweets to retrieve (10-100)
            
        Returns:
            List of tweet dictionaries with id, text, author, and metrics
        """
        try:
            # Adjust max_results to be within API limits
            max_results = min(max(max_results, 10), 100)
            
            response = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=['created_at', 'public_metrics', 'author_id'],
                expansions=['author_id'],
                user_fields=['username', 'name']
            )
            
            if not response.data:
                return []
            
            # Create a map of user IDs to user info
            users = {}
            if response.includes and 'users' in response.includes:
                users = {user.id: user for user in response.includes['users']}
            
            tweets = []
            for tweet in response.data:
                author = users.get(tweet.author_id)
                # Use empty dict as fallback if public_metrics is None
                metrics = tweet.public_metrics or {}
                tweets.append({
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'author': {
                        'id': tweet.author_id,
                        'username': author.username if author else 'unknown',
                        'name': author.name if author else 'Unknown'
                    },
                    'metrics': {
                        'likes': metrics.get('like_count', 0),
                        'retweets': metrics.get('retweet_count', 0),
                        'replies': metrics.get('reply_count', 0)
                    }
                })
            
            return tweets
            
        except tweepy.TweepyException as e:
            logger.error(f"Error searching tweets: {e}")
            return []
    
    def build_coin_query(self, coin_symbol: str, coin_name: str = None) -> str:
        """
        Build a search query for a meme coin.
        
        Args:
            coin_symbol: The coin symbol (e.g., 'DOGE', 'SHIB')
            coin_name: Optional full coin name (e.g., 'Dogecoin')
            
        Returns:
            Formatted search query string
        """
        # Build query with symbol
        query = f"(${coin_symbol} OR #{coin_symbol}"
        
        # Add coin name if provided
        if coin_name:
            query += f" OR {coin_name}"
        
        query += ") -is:retweet lang:en"
        
        return query
