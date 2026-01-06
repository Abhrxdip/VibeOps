"""
CSV Export Module
Handles exporting email processing data to CSV with proper formatting
"""

import csv
import io
from typing import List, Dict
from datetime import datetime


class CSVExporter:
    """Export processed email data to CSV format"""
    
    COLUMN_HEADERS = [
        'email_id',
        'sender',
        'sender_name',
        'subject',
        'received_at',
        'summary',
        'intent',
        'urgency',
        'sentiment',
        'selected_action',
        'drafted_reply',
        'processed_at'
    ]
    
    @classmethod
    def export_to_csv(cls, processed_emails: List[Dict], filename: str = None) -> str:
        """
        Export processed emails to CSV
        
        Args:
            processed_emails: List of processed email dictionaries
            filename: Optional filename (generates default if not provided)
            
        Returns:
            CSV content as string
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'mailmind_export_{timestamp}.csv'
        
        # Prepare data for export
        rows = []
        for email in processed_emails:
            row = {
                'email_id': email.get('email_id', ''),
                'sender': email.get('sender', ''),
                'sender_name': email.get('sender_name', ''),
                'subject': email.get('subject', ''),
                'received_at': cls._format_datetime(email.get('timestamp')),
                'summary': cls._clean_text(email.get('summary', '')),
                'intent': email.get('intent', ''),
                'urgency': email.get('urgency', ''),
                'sentiment': email.get('sentiment', ''),
                'selected_action': email.get('selected_action', 'None'),
                'drafted_reply': cls._clean_text(email.get('drafted_reply', '')),
                'processed_at': cls._format_datetime(email.get('processed_at', datetime.now()))
            }
            rows.append(row)
        
        # Create CSV string using csv module
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=cls.COLUMN_HEADERS, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)
        csv_string = output.getvalue()
        output.close()
        
        return csv_string, filename
    
    @classmethod
    def export_to_bytes(cls, processed_emails: List[Dict]) -> bytes:
        """
        Export to bytes for download
        
        Args:
            processed_emails: List of processed email dictionaries
            
        Returns:
            CSV content as bytes
        """
        csv_string, _ = cls.export_to_csv(processed_emails)
        return csv_string.encode('utf-8')
    
    @classmethod
    def _format_datetime(cls, dt) -> str:
        """Format datetime for CSV export"""
        if dt is None:
            return ''
        if isinstance(dt, str):
            return dt
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
    @classmethod
    def _clean_text(cls, text: str) -> str:
        """Clean text for CSV export (handle newlines and special chars)"""
        if not text:
            return ''
        
        # Replace problematic characters
        text = text.replace('\r\n', ' ')
        text = text.replace('\n', ' ')
        text = text.replace('\r', ' ')
        
        # Remove multiple spaces
        text = ' '.join(text.split())
        
        return text
    
    @classmethod
    def generate_statistics(cls, processed_emails: List[Dict]) -> Dict:
        """
        Generate statistics from processed emails
        
        Args:
            processed_emails: List of processed email dictionaries
            
        Returns:
            Dictionary with statistics
        """
        if not processed_emails:
            return {
                'total_emails': 0,
                'by_intent': {},
                'by_urgency': {},
                'by_sentiment': {},
                'processed_count': 0
            }
        
        # Count by categories without pandas
        intent_counts = {}
        urgency_counts = {}
        sentiment_counts = {}
        processed_count = 0
        
        for email in processed_emails:
            # Count intents
            intent = email.get('intent', '')
            if intent:
                intent_counts[intent] = intent_counts.get(intent, 0) + 1
            
            # Count urgency
            urgency = email.get('urgency', '')
            if urgency:
                urgency_counts[urgency] = urgency_counts.get(urgency, 0) + 1
            
            # Count sentiment
            sentiment = email.get('sentiment', '')
            if sentiment:
                sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
            
            # Count processed
            if email.get('processed_at'):
                processed_count += 1
        
        stats = {
            'total_emails': len(processed_emails),
            'by_intent': intent_counts,
            'by_urgency': urgency_counts,
            'by_sentiment': sentiment_counts,
            'processed_count': processed_count
        }
        
        return stats
