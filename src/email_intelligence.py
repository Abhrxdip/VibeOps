"""
AI-Powered Email Intelligence Module
Handles summarization, classification, and reply generation with fallback logic
"""

import asyncio
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

# Optional OpenAI import - only needed for AI features
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None

from config import Config


class EmailIntelligence:
    """AI-powered email analysis and processing"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI intelligence module
        
        Args:
            api_key: OpenAI API key (uses config if not provided)
        """
        self.api_key = api_key or Config.OPENAI_API_KEY
        
        # Check if OpenAI is available and configured
        if not OPENAI_AVAILABLE:
            self.use_ai = False
            print("OpenAI library not installed. Using rule-based processing.")
        elif self.api_key:
            openai.api_key = self.api_key
            self.use_ai = True
        else:
            self.use_ai = False
    
    async def process_email(self, email: Dict) -> Dict:
        """
        Process a single email with AI analysis
        
        Args:
            email: Email dictionary with subject, body, sender, timestamp
            
        Returns:
            Dictionary with summary, intent, urgency, sentiment, and replies
        """
        try:
            if self.use_ai:
                result = await self._ai_process_email(email)
            else:
                result = self._rule_based_process_email(email)
            
            return result
            
        except Exception as e:
            print(f"Error processing email {email.get('id', 'unknown')}: {e}")
            # Fallback to rule-based processing
            return self._rule_based_process_email(email)
    
    async def _ai_process_email(self, email: Dict) -> Dict:
        """Process email using OpenAI GPT"""
        
        email_text = f"""
Subject: {email.get('subject', 'No Subject')}
From: {email.get('sender_name', 'Unknown')} <{email.get('sender', 'unknown@example.com')}>
Date: {email.get('timestamp', datetime.now()).strftime('%Y-%m-%d %H:%M')}

Body:
{email.get('body', email.get('snippet', ''))}
"""
        
        prompt = f"""Analyze this email and provide a structured response in the following format:

SUMMARY: (3-5 lines summarizing the key points and any required actions)

INTENT: (Choose ONE: Informational, Action Required, Meeting Request, Follow-up, Spam/Low Priority)

URGENCY: (Choose ONE: High, Medium, Low)

SENTIMENT: (Choose ONE: Positive, Neutral, Negative)

SUGGESTED_REPLIES:
1. [Short reply option 1]
2. [Short reply option 2]
3. [Short reply option 3]

Email to analyze:
{email_text}
"""
        
        try:
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    openai.chat.completions.create,
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert email assistant that analyzes emails and provides concise, actionable insights."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                ),
                timeout=Config.AI_TIMEOUT_SECONDS
            )
            
            content = response.choices[0].message.content
            return self._parse_ai_response(content, email)
            
        except asyncio.TimeoutError:
            print(f"AI processing timeout for email {email.get('id')}")
            if Config.ENABLE_AI_FALLBACK:
                return self._rule_based_process_email(email)
            raise
        except Exception as e:
            print(f"AI processing error: {e}")
            if Config.ENABLE_AI_FALLBACK:
                return self._rule_based_process_email(email)
            raise
    
    def _parse_ai_response(self, response: str, email: Dict) -> Dict:
        """Parse structured AI response"""
        
        result = {
            'summary': '',
            'intent': 'Informational',
            'urgency': 'Medium',
            'sentiment': 'Neutral',
            'suggested_replies': []
        }
        
        lines = response.strip().split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('SUMMARY:'):
                result['summary'] = line.replace('SUMMARY:', '').strip()
                current_section = 'summary'
            elif line.startswith('INTENT:'):
                intent = line.replace('INTENT:', '').strip()
                if intent in Config.INTENT_CATEGORIES:
                    result['intent'] = intent
                current_section = None
            elif line.startswith('URGENCY:'):
                urgency = line.replace('URGENCY:', '').strip()
                if urgency in Config.URGENCY_LEVELS:
                    result['urgency'] = urgency
                current_section = None
            elif line.startswith('SENTIMENT:'):
                sentiment = line.replace('SENTIMENT:', '').strip()
                if sentiment in Config.SENTIMENT_TAGS:
                    result['sentiment'] = sentiment
                current_section = None
            elif line.startswith('SUGGESTED_REPLIES:'):
                current_section = 'replies'
            elif current_section == 'summary' and line:
                result['summary'] += ' ' + line
            elif current_section == 'replies' and line:
                # Extract numbered replies
                reply = re.sub(r'^\d+\.\s*', '', line).strip('[]')
                if reply:
                    result['suggested_replies'].append(reply)
        
        # Ensure we have a summary
        if not result['summary']:
            result['summary'] = self._generate_basic_summary(email)
        
        # Ensure we have at least one reply
        if not result['suggested_replies']:
            result['suggested_replies'] = self._generate_template_replies(
                result['intent']
            )
        
        return result
    
    def _rule_based_process_email(self, email: Dict) -> Dict:
        """Process email using rule-based classification (fallback)"""
        
        subject = email.get('subject', '').lower()
        body = email.get('body', email.get('snippet', '')).lower()
        timestamp = email.get('timestamp', datetime.now())
        full_text = f"{subject} {body}"
        
        # Classify intent
        intent = self._classify_intent(full_text)
        
        # Classify urgency
        urgency = self._classify_urgency(full_text, timestamp)
        
        # Classify sentiment
        sentiment = self._classify_sentiment(full_text)
        
        # Generate summary
        summary = self._generate_basic_summary(email)
        
        # Generate suggested replies
        suggested_replies = self._generate_template_replies(intent)
        
        return {
            'summary': summary,
            'intent': intent,
            'urgency': urgency,
            'sentiment': sentiment,
            'suggested_replies': suggested_replies
        }
    
    def _classify_intent(self, text: str) -> str:
        """Rule-based intent classification"""
        
        # Spam/Low Priority indicators
        spam_keywords = ['winner', 'congratulations!!!', 'claim your prize', 
                        'click here', 'limited time', 'act now', '$$$']
        if any(keyword in text for keyword in spam_keywords):
            return 'Spam/Low Priority'
        
        # Meeting Request indicators
        meeting_keywords = ['meeting', 'schedule', 'calendar', 'availability',
                          'call', 'conference', 'zoom', 'teams']
        if any(keyword in text for keyword in meeting_keywords):
            return 'Meeting Request'
        
        # Action Required indicators
        action_keywords = ['urgent', 'asap', 'action required', 'please', 
                          'need', 'must', 'required', 'approve', 'confirm']
        if any(keyword in text for keyword in action_keywords):
            return 'Action Required'
        
        # Follow-up indicators
        followup_keywords = ['follow up', 'following up', 're:', 'regarding',
                            'update', 'status', 'checking in']
        if any(keyword in text for keyword in followup_keywords):
            return 'Follow-up'
        
        # Default to Informational
        return 'Informational'
    
    def _classify_urgency(self, text: str, timestamp: datetime) -> str:
        """Rule-based urgency classification"""
        
        # High urgency indicators
        urgent_keywords = ['urgent', 'asap', 'immediately', 'critical',
                          'emergency', 'today', 'deadline', 'must']
        
        # Check if email is very recent (< 3 hours)
        is_recent = (datetime.now() - timestamp) < timedelta(hours=3)
        
        if any(keyword in text for keyword in urgent_keywords) or is_recent:
            return 'High'
        
        # Low urgency indicators
        low_keywords = ['fyi', 'for your information', 'newsletter', 
                       'update', 'digest', 'no action required']
        
        # Check if email is old (> 48 hours)
        is_old = (datetime.now() - timestamp) > timedelta(hours=48)
        
        if any(keyword in text for keyword in low_keywords) or is_old:
            return 'Low'
        
        # Default to Medium
        return 'Medium'
    
    def _classify_sentiment(self, text: str) -> str:
        """Rule-based sentiment classification"""
        
        # Positive indicators
        positive_keywords = ['thank', 'excellent', 'great', 'wonderful',
                           'appreciate', 'impressed', 'congratulations',
                           'happy', 'pleased', 'perfect']
        positive_count = sum(1 for keyword in positive_keywords if keyword in text)
        
        # Negative indicators
        negative_keywords = ['issue', 'problem', 'error', 'failed', 'wrong',
                           'disappointed', 'concerned', 'urgent', 'critical',
                           'complaint']
        negative_count = sum(1 for keyword in negative_keywords if keyword in text)
        
        if positive_count > negative_count and positive_count > 0:
            return 'Positive'
        elif negative_count > positive_count and negative_count > 0:
            return 'Negative'
        else:
            return 'Neutral'
    
    def _generate_basic_summary(self, email: Dict) -> str:
        """Generate a basic summary from email content"""
        
        subject = email.get('subject', 'No Subject')
        body = email.get('body', email.get('snippet', ''))
        sender_name = email.get('sender_name', 'Unknown')
        
        # Extract first few sentences from body
        sentences = re.split(r'[.!?]+', body)
        key_sentences = [s.strip() for s in sentences[:3] if s.strip()]
        
        summary = f"{sender_name} sent an email regarding: {subject}. "
        
        if key_sentences:
            summary += ' '.join(key_sentences[:2])
            if len(summary) > 250:
                summary = summary[:247] + '...'
        
        return summary
    
    def _generate_template_replies(self, intent: str) -> List[str]:
        """Generate template-based replies based on intent"""
        
        base_replies = [
            Config.REPLY_TEMPLATES['acknowledged'],
            Config.REPLY_TEMPLATES['thank_you']
        ]
        
        if intent == 'Action Required':
            base_replies = [
                Config.REPLY_TEMPLATES['review'],
                Config.REPLY_TEMPLATES['acknowledged'],
                Config.REPLY_TEMPLATES['need_more_info']
            ]
        elif intent == 'Meeting Request':
            base_replies = [
                Config.REPLY_TEMPLATES['meeting_confirmed'],
                "Let me check my calendar and get back to you.",
                "Could we schedule this for next week instead?"
            ]
        elif intent == 'Follow-up':
            base_replies = [
                Config.REPLY_TEMPLATES['review'],
                Config.REPLY_TEMPLATES['thank_you'],
                "Thanks for the follow-up. I'll prioritize this."
            ]
        elif intent == 'Spam/Low Priority':
            base_replies = [
                Config.REPLY_TEMPLATES['not_relevant'],
                "Please remove me from this mailing list.",
                "Not interested, thank you."
            ]
        
        return base_replies[:3]
    
    async def process_batch(self, emails: List[Dict]) -> List[Dict]:
        """
        Process multiple emails concurrently
        
        Args:
            emails: List of email dictionaries
            
        Returns:
            List of processed email results
        """
        tasks = [self.process_email(email) for email in emails]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Error processing email {i}: {result}")
                # Use fallback
                processed_results.append(
                    self._rule_based_process_email(emails[i])
                )
            else:
                processed_results.append(result)
        
        return processed_results
