"""
MailMind Configuration Module
Loads environment variables and application settings
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
    
    # Gmail API
    GMAIL_CREDENTIALS_PATH = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')
    GMAIL_TOKEN_PATH = 'token.pickle'
    GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    # Application Settings
    USE_MOCK_DATA = os.getenv('USE_MOCK_DATA', 'true').lower() == 'true'
    MAX_EMAILS_PER_BATCH = int(os.getenv('MAX_EMAILS_PER_BATCH', '50'))
    AI_TIMEOUT_SECONDS = int(os.getenv('AI_TIMEOUT_SECONDS', '30'))
    ENABLE_AI_FALLBACK = os.getenv('ENABLE_AI_FALLBACK', 'true').lower() == 'true'
    
    # Intent Categories
    INTENT_CATEGORIES = [
        'Informational',
        'Action Required',
        'Meeting Request',
        'Follow-up',
        'Spam/Low Priority'
    ]
    
    # Urgency Levels
    URGENCY_LEVELS = ['High', 'Medium', 'Low']
    
    # Sentiment Tags
    SENTIMENT_TAGS = ['Positive', 'Neutral', 'Negative']
    
    # Reply Templates
    REPLY_TEMPLATES = {
        'thank_you': 'Thank you for the update. I appreciate you keeping me informed.',
        'review': "I'll review this and get back to you shortly.",
        'meeting_confirmed': 'Meeting confirmed. Looking forward to it.',
        'need_more_info': 'Could you please provide more details on this?',
        'acknowledged': 'Acknowledged. I will handle this accordingly.',
        'not_relevant': 'Thank you, but this doesn\'t require action from me at this time.'
    }
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.USE_MOCK_DATA:
            if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
                raise ValueError("Either OPENAI_API_KEY or ANTHROPIC_API_KEY must be set when not using mock data")
            
            gmail_creds_path = Path(cls.GMAIL_CREDENTIALS_PATH)
            if not gmail_creds_path.exists():
                print(f"Warning: Gmail credentials file not found at {cls.GMAIL_CREDENTIALS_PATH}")
                print("Falling back to mock data mode")
                cls.USE_MOCK_DATA = True
