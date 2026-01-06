"""
Advanced Features Module
Unique and creative email intelligence features
"""

import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import Counter
import hashlib


class EmailPatternAnalyzer:
    """Analyzes communication patterns and behavioral insights"""
    
    @staticmethod
    def detect_communication_style(email: Dict) -> Dict:
        """
        Detect sender's communication style and personality traits
        
        Returns:
            Style profile with formality, emotion, complexity scores
        """
        body = email.get('body', '').lower()
        subject = email.get('subject', '').lower()
        combined = f"{subject} {body}"
        
        # Formality detection
        formal_markers = ['dear', 'sincerely', 'regards', 'respectfully', 'kindly', 'pursuant', 'herewith']
        casual_markers = ['hey', 'hi there', 'thanks!', 'cheers', 'awesome', 'cool', 'lol', 'btw']
        
        formal_count = sum(1 for marker in formal_markers if marker in combined)
        casual_count = sum(1 for marker in casual_markers if marker in combined)
        
        formality_score = min(100, max(0, 50 + (formal_count * 15) - (casual_count * 15)))
        
        # Emotion detection
        positive_words = ['happy', 'great', 'excellent', 'wonderful', 'pleased', 'excited', 'thank', 'appreciate']
        negative_words = ['unfortunately', 'concern', 'issue', 'problem', 'disappointed', 'worried', 'sorry']
        urgent_words = ['urgent', 'asap', 'immediately', 'critical', 'emergency', 'deadline', 'now']
        
        emotion = 'neutral'
        if any(word in combined for word in urgent_words):
            emotion = 'urgent'
        elif any(word in combined for word in negative_words):
            emotion = 'concerned'
        elif any(word in combined for word in positive_words):
            emotion = 'positive'
        
        # Complexity score (reading difficulty)
        words = combined.split()
        avg_word_length = sum(len(word) for word in words) / max(len(words), 1)
        sentences = combined.count('.') + combined.count('!') + combined.count('?')
        complexity_score = min(100, int((avg_word_length * 10) + (len(words) / max(sentences, 1))))
        
        # Communication pace
        exclamation_count = body.count('!')
        question_count = body.count('?')
        
        if exclamation_count > 2:
            pace = 'energetic'
        elif question_count > 3:
            pace = 'inquisitive'
        elif len(words) < 50:
            pace = 'concise'
        else:
            pace = 'detailed'
        
        return {
            'formality_score': formality_score,
            'formality_level': 'formal' if formality_score > 60 else 'casual' if formality_score < 40 else 'balanced',
            'emotion': emotion,
            'complexity_score': complexity_score,
            'reading_difficulty': 'complex' if complexity_score > 70 else 'moderate' if complexity_score > 40 else 'simple',
            'communication_pace': pace,
            'word_count': len(words),
            'estimated_read_time': f"{max(1, len(words) // 200)} min"
        }
    
    @staticmethod
    def extract_entities(email: Dict) -> Dict:
        """Extract important entities from email"""
        body = email.get('body', '')
        
        # Extract dates
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b'
        ]
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, body, re.IGNORECASE))
        
        # Extract times
        time_pattern = r'\b\d{1,2}:\d{2}(?:\s*[AP]M)?\b'
        times = re.findall(time_pattern, body, re.IGNORECASE)
        
        # Extract monetary amounts
        money_pattern = r'\$\d+(?:,\d{3})*(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:dollars|USD|EUR|GBP)'
        amounts = re.findall(money_pattern, body, re.IGNORECASE)
        
        # Extract phone numbers
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, body)
        
        # Extract URLs
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, body)
        
        # Extract action verbs
        action_verbs = ['review', 'approve', 'sign', 'submit', 'send', 'confirm', 'update', 'schedule', 'attend', 'complete']
        actions = [verb for verb in action_verbs if verb in body.lower()]
        
        return {
            'dates': dates[:3],  # Top 3
            'times': times[:3],
            'monetary_amounts': amounts[:3],
            'phone_numbers': phones,
            'urls': urls[:2],
            'action_items': actions,
            'has_attachments': 'attachment' in body.lower() or 'attached' in body.lower()
        }
    
    @staticmethod
    def predict_response_time(email: Dict) -> Dict:
        """Predict optimal response time and generate deadline"""
        urgency = email.get('urgency', 'medium')
        intent = email.get('intent', 'information')
        
        # Base response times (in hours)
        urgency_times = {
            'high': 2,
            'medium': 24,
            'low': 72
        }
        
        intent_multipliers = {
            'action_required': 1.0,
            'meeting_request': 0.5,
            'question': 0.8,
            'information': 1.5,
            'urgent': 0.3
        }
        
        base_hours = urgency_times.get(urgency, 24)
        multiplier = intent_multipliers.get(intent, 1.0)
        recommended_hours = base_hours * multiplier
        
        deadline = datetime.now() + timedelta(hours=recommended_hours)
        
        # Priority scoring
        priority_score = 100 - recommended_hours * 2
        priority_score = max(0, min(100, priority_score))
        
        return {
            'recommended_response_hours': recommended_hours,
            'deadline': deadline.strftime('%Y-%m-%d %I:%M %p'),
            'priority_score': int(priority_score),
            'urgency_label': 'CRITICAL' if recommended_hours <= 2 else 'HIGH' if recommended_hours <= 8 else 'NORMAL' if recommended_hours <= 24 else 'LOW'
        }
    
    @staticmethod
    def calculate_thread_score(emails: List[Dict]) -> Dict:
        """Calculate email thread importance and engagement metrics"""
        if not emails:
            return {}
        
        senders = [e.get('sender', '') for e in emails]
        sender_frequency = Counter(senders)
        
        total_words = sum(len(e.get('body', '').split()) for e in emails)
        avg_response_time = len(emails) * 4  # Simplified calculation
        
        # Thread intensity score
        thread_score = min(100, len(emails) * 10 + (total_words // 100))
        
        return {
            'thread_length': len(emails),
            'unique_participants': len(sender_frequency),
            'most_active_sender': sender_frequency.most_common(1)[0][0] if sender_frequency else 'Unknown',
            'total_word_count': total_words,
            'thread_intensity_score': thread_score,
            'estimated_importance': 'critical' if thread_score > 70 else 'high' if thread_score > 40 else 'moderate'
        }


class SmartCategorizer:
    """Advanced categorization beyond basic intent detection"""
    
    @staticmethod
    def detect_email_category(email: Dict) -> str:
        """Detect granular email categories"""
        subject = email.get('subject', '').lower()
        body = email.get('body', '').lower()
        combined = f"{subject} {body}"
        
        categories = {
            '💼 Business': ['proposal', 'contract', 'agreement', 'invoice', 'payment', 'business'],
            '📅 Calendar': ['meeting', 'appointment', 'schedule', 'calendar', 'event', 'reschedule'],
            '🎯 Project': ['project', 'milestone', 'deliverable', 'sprint', 'task', 'deadline'],
            '💰 Financial': ['budget', 'expense', 'cost', 'financial', 'revenue', 'invoice', 'payment'],
            '👥 HR': ['interview', 'candidate', 'recruitment', 'onboarding', 'performance', 'leave'],
            '🔧 Technical': ['bug', 'issue', 'error', 'deployment', 'code', 'technical', 'system'],
            '📢 Marketing': ['campaign', 'promotion', 'announcement', 'launch', 'social media'],
            '🎓 Training': ['training', 'workshop', 'webinar', 'course', 'learning', 'certification'],
            '⚠️ Alert': ['alert', 'warning', 'critical', 'security', 'incident', 'breach'],
            '📄 Documentation': ['report', 'documentation', 'policy', 'procedure', 'guidelines'],
        }
        
        for category, keywords in categories.items():
            if any(keyword in combined for keyword in keywords):
                return category
        
        return '📬 General'
    
    @staticmethod
    def detect_sender_relationship(email: Dict) -> str:
        """Infer relationship with sender"""
        sender = email.get('sender', '').lower()
        body = email.get('body', '').lower()
        
        if any(word in body for word in ['team', 'colleague', 'department']):
            return '👥 Colleague'
        elif any(word in body for word in ['client', 'customer', 'partner']):
            return '🤝 External Partner'
        elif any(word in body for word in ['manager', 'director', 'vp', 'ceo']):
            return '👔 Leadership'
        elif '@' not in sender or sender.endswith(('.com', '.org', '.net')):
            return '🏢 Internal'
        else:
            return '🌐 External'


class EmailInsightGenerator:
    """Generate unique insights and recommendations"""
    
    @staticmethod
    def generate_executive_summary(emails: List[Dict]) -> Dict:
        """Create high-level executive dashboard metrics"""
        if not emails:
            return {}
        
        total = len(emails)
        high_urgency = sum(1 for e in emails if e.get('urgency') == 'high')
        action_required = sum(1 for e in emails if e.get('intent') == 'action_required')
        
        # Calculate workload score
        workload_score = (high_urgency * 3 + action_required * 2) * 10
        workload_score = min(100, workload_score)
        
        # Response burden
        total_words = sum(len(e.get('body', '').split()) for e in emails)
        estimated_processing_time = (total * 2) + (total_words // 200)  # minutes
        
        # Risk score
        urgent_count = sum(1 for e in emails if 'urgent' in e.get('body', '').lower())
        deadline_count = sum(1 for e in emails if 'deadline' in e.get('body', '').lower())
        risk_score = min(100, (urgent_count + deadline_count) * 15)
        
        return {
            'total_emails': total,
            'high_priority_count': high_urgency,
            'action_required_count': action_required,
            'workload_score': workload_score,
            'workload_level': 'OVERLOADED' if workload_score > 70 else 'BUSY' if workload_score > 40 else 'MANAGEABLE',
            'estimated_processing_minutes': estimated_processing_time,
            'risk_score': risk_score,
            'risk_level': 'HIGH' if risk_score > 60 else 'MODERATE' if risk_score > 30 else 'LOW',
            'recommendation': EmailInsightGenerator._get_recommendation(workload_score, risk_score)
        }
    
    @staticmethod
    def _get_recommendation(workload: int, risk: int) -> str:
        """Generate actionable recommendation"""
        if workload > 70 and risk > 60:
            return "🚨 URGENT: Prioritize high-risk items immediately. Consider delegating low-priority tasks."
        elif workload > 70:
            return "⚡ High workload detected. Focus on action-required emails first."
        elif risk > 60:
            return "⚠️ Multiple urgent items need attention. Review deadlines carefully."
        elif workload > 40:
            return "📊 Moderate workload. Batch process similar emails for efficiency."
        else:
            return "✅ Inbox under control. Good time for strategic planning."
    
    @staticmethod
    def detect_email_chains(emails: List[Dict]) -> List[Dict]:
        """Detect related email chains and threads"""
        chains = []
        processed = set()
        
        for i, email in enumerate(emails):
            if i in processed:
                continue
            
            subject = email.get('subject', '').lower()
            subject_clean = re.sub(r'^(re:|fwd:)\s*', '', subject).strip()
            
            # Find related emails
            chain = [email]
            for j, other in enumerate(emails[i+1:], start=i+1):
                other_subject = other.get('subject', '').lower()
                other_clean = re.sub(r'^(re:|fwd:)\s*', '', other_subject).strip()
                
                if subject_clean == other_clean or subject_clean in other_clean or other_clean in subject_clean:
                    chain.append(other)
                    processed.add(j)
            
            if len(chain) > 1:
                chains.append({
                    'subject': email.get('subject', 'No Subject'),
                    'thread_size': len(chain),
                    'emails': chain
                })
        
        return sorted(chains, key=lambda x: x['thread_size'], reverse=True)
