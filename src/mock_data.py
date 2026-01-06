"""
Mock Email Data Generator
Provides sample emails for testing without Gmail API
"""

from datetime import datetime, timedelta
from typing import List, Dict
import random

class MockEmailGenerator:
    """Generate realistic mock email data"""
    
    SAMPLE_EMAILS = [
        {
            'id': 'mock_001',
            'sender': 'john.smith@company.com',
            'sender_name': 'John Smith',
            'subject': 'Urgent: Q4 Budget Review Meeting',
            'body': '''Hi Team,

We need to schedule an urgent meeting to review the Q4 budget allocations. There are some significant variances that need immediate attention.

Please confirm your availability for tomorrow at 2 PM EST. This is high priority and requires everyone's presence.

Key points to discuss:
- Marketing overspend by 15%
- IT infrastructure needs
- Resource reallocation proposals

Thanks,
John''',
            'timestamp': datetime.now() - timedelta(hours=2),
            'labels': ['UNREAD', 'IMPORTANT']
        },
        {
            'id': 'mock_002',
            'sender': 'newsletter@techinsights.com',
            'sender_name': 'Tech Insights Weekly',
            'subject': 'Weekly Tech Digest: AI Trends 2025',
            'body': '''Hello Subscriber,

Here's your weekly roundup of the latest in technology:

1. AI Agents Transform Business Operations
2. Cloud Computing Costs Continue to Rise
3. Cybersecurity Best Practices for Remote Teams
4. The Future of Low-Code Development

Read more at our website.

Best regards,
Tech Insights Team''',
            'timestamp': datetime.now() - timedelta(days=1),
            'labels': ['UNREAD']
        },
        {
            'id': 'mock_003',
            'sender': 'sarah.johnson@client.com',
            'sender_name': 'Sarah Johnson',
            'subject': 'RE: Project Milestone Delivery',
            'body': '''Hi,

Thank you for delivering the first milestone ahead of schedule. The quality of work is excellent and the stakeholders are very impressed.

For the next phase, could you provide:
1. Updated timeline
2. Resource requirements
3. Risk assessment

Looking forward to continuing our collaboration.

Best,
Sarah''',
            'timestamp': datetime.now() - timedelta(hours=5),
            'labels': ['UNREAD', 'IMPORTANT']
        },
        {
            'id': 'mock_004',
            'sender': 'hr@company.com',
            'sender_name': 'HR Department',
            'subject': 'FYI: Updated PTO Policy 2025',
            'body': '''Dear Team,

This is to inform you about updates to our Paid Time Off policy effective January 1, 2025:

- Increased annual PTO days from 15 to 18
- New parental leave benefits
- Flexible holiday scheduling
- Rollover policy changes

Full details are available on the employee portal. No action required at this time.

HR Team''',
            'timestamp': datetime.now() - timedelta(days=3),
            'labels': ['UNREAD']
        },
        {
            'id': 'mock_005',
            'sender': 'mike.brown@vendor.com',
            'sender_name': 'Mike Brown',
            'subject': 'Follow-up: Contract Renewal Discussion',
            'body': '''Hi,

Following up on our conversation last week regarding the contract renewal. We've prepared the updated terms and pricing.

Can we schedule a call this week to go over the details? I'm available Tuesday through Thursday afternoons.

Please let me know what works best for you.

Regards,
Mike''',
            'timestamp': datetime.now() - timedelta(hours=8),
            'labels': ['UNREAD']
        },
        {
            'id': 'mock_006',
            'sender': 'security@company.com',
            'sender_name': 'IT Security',
            'subject': 'URGENT: Security Patch Required',
            'body': '''IMMEDIATE ACTION REQUIRED

A critical security vulnerability has been identified in our VPN software. You must install the security patch by end of day today.

Steps:
1. Close all applications
2. Run the Security Update tool from IT portal
3. Restart your computer
4. Confirm completion by replying to this email

Failure to comply may result in account suspension for security reasons.

IT Security Team''',
            'timestamp': datetime.now() - timedelta(minutes=30),
            'labels': ['UNREAD', 'IMPORTANT']
        },
        {
            'id': 'mock_007',
            'sender': 'events@company.com',
            'sender_name': 'Events Team',
            'subject': 'Invitation: Annual Company Holiday Party',
            'body': '''You're Invited!

Join us for our Annual Holiday Celebration on December 15th at 6 PM at the Grand Ballroom.

This year's theme: Winter Wonderland

- Dinner and drinks
- Live entertainment
- Awards ceremony
- Secret Santa gift exchange ($25 limit)

RSVP by December 1st. Plus-one welcome!

Event Team''',
            'timestamp': datetime.now() - timedelta(days=5),
            'labels': ['UNREAD']
        },
        {
            'id': 'mock_008',
            'sender': 'spam@promo-deals.xyz',
            'sender_name': 'Amazing Deals',
            'subject': '🎉 You WON! Claim Your Prize NOW!!!',
            'body': '''CONGRATULATIONS!!!

You have been selected as our LUCKY WINNER! Claim your $1000 gift card NOW by clicking the link below.

CLICK HERE TO CLAIM YOUR PRIZE!!!

This offer expires in 24 hours. Don't miss out on this amazing opportunity!

*Terms and conditions apply. Must provide credit card for verification.''',
            'timestamp': datetime.now() - timedelta(days=2),
            'labels': ['UNREAD', 'SPAM']
        },
        {
            'id': 'mock_009',
            'sender': 'emma.davis@partner.com',
            'sender_name': 'Emma Davis',
            'subject': 'Quick question about API integration',
            'body': '''Hey,

Quick question - I'm working on integrating our systems with your API and running into an authentication issue with OAuth2.

The error message says "invalid_grant" when trying to refresh the access token. Could you point me to the right documentation or let me know if there's a known issue?

Not urgent, but would appreciate guidance when you have a moment.

Thanks!
Emma''',
            'timestamp': datetime.now() - timedelta(hours=12),
            'labels': ['UNREAD']
        },
        {
            'id': 'mock_010',
            'sender': 'ceo@company.com',
            'sender_name': 'CEO',
            'subject': 'All-Hands Meeting: Company Direction 2025',
            'body': '''Team,

I'm scheduling an all-hands meeting for next Monday at 10 AM to discuss our strategic direction for 2025.

Agenda:
- Year-end review and achievements
- 2025 objectives and key results
- Organizational changes
- Q&A session

This is mandatory attendance. The meeting will be recorded for those traveling.

We've accomplished great things this year and I'm excited to share our vision for the future.

CEO''',
            'timestamp': datetime.now() - timedelta(hours=3),
            'labels': ['UNREAD', 'IMPORTANT']
        }
    ]
    
    @classmethod
    def get_mock_emails(cls, count: int = None) -> List[Dict]:
        """
        Get mock email data
        
        Args:
            count: Number of emails to return (None for all)
            
        Returns:
            List of mock email dictionaries
        """
        emails = cls.SAMPLE_EMAILS.copy()
        
        if count is not None:
            emails = random.sample(emails, min(count, len(emails)))
        
        return emails
    
    @classmethod
    def add_random_emails(cls, count: int = 5) -> List[Dict]:
        """Generate additional random emails"""
        
        subjects_pool = [
            "RE: Your recent inquiry",
            "Meeting notes from yesterday",
            "Project update - Week 45",
            "FYI: System maintenance scheduled",
            "Action required: Approve timesheet",
            "Question about documentation",
            "Quarterly review reminder",
            "Team lunch next Friday?",
            "Updated guidelines available",
            "Congratulations on your achievement"
        ]
        
        senders_pool = [
            ("alex.wilson@example.com", "Alex Wilson"),
            ("jennifer.taylor@client.org", "Jennifer Taylor"),
            ("david.martinez@vendor.net", "David Martinez"),
            ("lisa.anderson@company.com", "Lisa Anderson"),
            ("robert.thomas@partner.io", "Robert Thomas")
        ]
        
        random_emails = []
        base_id = len(cls.SAMPLE_EMAILS) + 1
        
        for i in range(count):
            sender, sender_name = random.choice(senders_pool)
            subject = random.choice(subjects_pool)
            
            random_emails.append({
                'id': f'mock_{base_id + i:03d}',
                'sender': sender,
                'sender_name': sender_name,
                'subject': subject,
                'body': f'This is a randomly generated email for testing purposes.\n\nContent of email {i+1}.',
                'timestamp': datetime.now() - timedelta(hours=random.randint(1, 72)),
                'labels': ['UNREAD']
            })
        
        return random_emails
