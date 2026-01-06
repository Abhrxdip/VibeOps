"""
Gmail API Integration Module
Handles read-only Gmail API access with fallback to mock data
"""

import pickle
import os.path
from typing import List, Dict, Optional
from datetime import datetime
import base64
from email.mime.text import MIMEText

# Optional Gmail API imports - only needed for real Gmail integration
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False
    Request = None
    Credentials = None
    InstalledAppFlow = None
    build = None
    HttpError = Exception

from config import Config
from mock_data import MockEmailGenerator


class GmailFetcher:
    """Fetch emails from Gmail API or mock data"""
    
    def __init__(self, use_mock: bool = None):
        """
        Initialize Gmail fetcher
        
        Args:
            use_mock: Force mock mode (overrides config)
        """
        # Force mock mode if Gmail API is not available
        if not GMAIL_AVAILABLE:
            self.use_mock = True
            print("Gmail API libraries not installed. Using mock data mode.")
        else:
            self.use_mock = use_mock if use_mock is not None else Config.USE_MOCK_DATA
        
        self.service = None
        
        if not self.use_mock:
            try:
                self._authenticate()
            except Exception as e:
                print(f"Gmail authentication failed: {e}")
                print("Falling back to mock data mode")
                self.use_mock = True
    
    def _authenticate(self):
        """Authenticate with Gmail API using OAuth2"""
        creds = None
        
        # Load existing credentials
        if os.path.exists(Config.GMAIL_TOKEN_PATH):
            with open(Config.GMAIL_TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(Config.GMAIL_CREDENTIALS_PATH):
                    raise FileNotFoundError(
                        f"Gmail credentials file not found: {Config.GMAIL_CREDENTIALS_PATH}"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    Config.GMAIL_CREDENTIALS_PATH,
                    Config.GMAIL_SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials for future use
            with open(Config.GMAIL_TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('gmail', 'v1', credentials=creds)
    
    def fetch_emails(self, max_results: int = None, label: str = 'UNREAD') -> List[Dict]:
        """
        Fetch emails from Gmail or mock data
        
        Args:
            max_results: Maximum number of emails to fetch
            label: Gmail label filter (default: UNREAD)
            
        Returns:
            List of email dictionaries
        """
        if max_results is None:
            max_results = Config.MAX_EMAILS_PER_BATCH
        
        if self.use_mock:
            return self._fetch_mock_emails(max_results)
        else:
            return self._fetch_gmail_emails(max_results, label)
    
    def _fetch_mock_emails(self, max_results: int) -> List[Dict]:
        """Fetch mock email data"""
        emails = MockEmailGenerator.get_mock_emails(max_results)
        
        # Format for consistency with Gmail API structure
        formatted_emails = []
        for email in emails:
            formatted_emails.append({
                'id': email['id'],
                'sender': email['sender'],
                'sender_name': email['sender_name'],
                'subject': email['subject'],
                'body': email['body'],
                'snippet': email['body'][:150],
                'timestamp': email['timestamp'],
                'labels': email.get('labels', ['UNREAD']),
                'is_mock': True
            })
        
        return formatted_emails
    
    def _fetch_gmail_emails(self, max_results: int, label: str) -> List[Dict]:
        """Fetch emails from Gmail API"""
        try:
            # Query for emails with specified label
            query = f'label:{label}'
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                print('No messages found.')
                return []
            
            emails = []
            for message in messages:
                email_data = self._get_email_details(message['id'])
                if email_data:
                    emails.append(email_data)
            
            return emails
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []
    
    def _get_email_details(self, message_id: str) -> Optional[Dict]:
        """Get detailed information for a specific email"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            headers = message['payload'].get('headers', [])
            
            # Extract key headers
            subject = ''
            sender = ''
            date_str = ''
            
            for header in headers:
                name = header['name'].lower()
                if name == 'subject':
                    subject = header['value']
                elif name == 'from':
                    sender = header['value']
                elif name == 'date':
                    date_str = header['value']
            
            # Extract email body
            body = self._get_email_body(message['payload'])
            snippet = message.get('snippet', '')
            
            # Parse timestamp
            timestamp = self._parse_date(date_str) if date_str else datetime.now()
            
            # Extract sender email and name
            sender_email, sender_name = self._parse_sender(sender)
            
            return {
                'id': message_id,
                'sender': sender_email,
                'sender_name': sender_name,
                'subject': subject,
                'body': body,
                'snippet': snippet,
                'timestamp': timestamp,
                'labels': message.get('labelIds', []),
                'is_mock': False
            }
            
        except HttpError as error:
            print(f'Error fetching email {message_id}: {error}')
            return None
    
    def _get_email_body(self, payload: Dict) -> str:
        """Extract email body from payload"""
        body = ''
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8')
                        break
                elif part['mimeType'] == 'text/html' and not body:
                    if 'data' in part['body']:
                        # Fallback to HTML if plain text not available
                        body = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8')
        else:
            if 'data' in payload.get('body', {}):
                body = base64.urlsafe_b64decode(
                    payload['body']['data']
                ).decode('utf-8')
        
        return body
    
    def _parse_sender(self, sender_str: str) -> tuple:
        """Parse sender string into email and name"""
        # Format: "Name <email@domain.com>" or "email@domain.com"
        if '<' in sender_str and '>' in sender_str:
            name = sender_str.split('<')[0].strip().strip('"')
            email = sender_str.split('<')[1].strip('>')
        else:
            email = sender_str.strip()
            name = email.split('@')[0]
        
        return email, name
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse email date string to datetime"""
        from email.utils import parsedate_to_datetime
        try:
            return parsedate_to_datetime(date_str)
        except:
            return datetime.now()
    
    def get_email_count(self, label: str = 'UNREAD') -> int:
        """Get count of emails with specified label"""
        if self.use_mock:
            return len(MockEmailGenerator.get_mock_emails())
        
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=f'label:{label}',
                maxResults=1
            ).execute()
            
            return results.get('resultSizeEstimate', 0)
        except:
            return 0
