"""
MailMind - Neural Email Intelligence Platform
Advanced AI-Powered Email Decision Layer
"""

import streamlit as st
import asyncio
from datetime import datetime
from typing import Dict, List

from config import Config
from gmail_fetcher import GmailFetcher
from email_intelligence import EmailIntelligence
from csv_exporter import CSVExporter
from advanced_features import EmailPatternAnalyzer, SmartCategorizer, EmailInsightGenerator


# Page configuration
st.set_page_config(
    page_title="MailMind - Neural Email Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .tagline {
        text-align: center;
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .email-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 6px solid #667eea;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .email-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .urgency-high {
        border-left-color: #ff6b6b !important;
        background: linear-gradient(135deg, #fff5f5 0%, #ffe0e0 100%) !important;
    }
    .urgency-medium {
        border-left-color: #ffd93d !important;
        background: linear-gradient(135deg, #fffef5 0%, #fff4d0 100%) !important;
    }
    .urgency-low {
        border-left-color: #51cf66 !important;
        background: linear-gradient(135deg, #f5fff5 0%, #d0f0d0 100%) !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    .insight-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
    }
    .pattern-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 3px;
    }
    .reply-button {
        margin: 5px;
        transition: all 0.3s;
    }
    .reply-button:hover {
        transform: scale(1.05);
    }
    .progress-ring {
        stroke-dasharray: 251.2;
        stroke-dashoffset: 0;
        transition: stroke-dashoffset 1s;
    }
    .entity-tag {
        background: #e3f2fd;
        color: #1976d2;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin: 2px;
        display: inline-block;
    }
    .risk-indicator {
        width: 100%;
        height: 8px;
        background: #e0e0e0;
        border-radius: 4px;
        overflow: hidden;
    }
    .risk-fill {
        height: 100%;
        transition: width 1s ease;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    """Initialize Streamlit session state variables"""
    if 'emails' not in st.session_state:
        st.session_state.emails = []
    if 'processed_emails' not in st.session_state:
        st.session_state.processed_emails = {}
    if 'selected_email_id' not in st.session_state:
        st.session_state.selected_email_id = None
    if 'filter_urgency' not in st.session_state:
        st.session_state.filter_urgency = 'All'
    if 'filter_intent' not in st.session_state:
        st.session_state.filter_intent = 'All'
    if 'fetcher' not in st.session_state:
        st.session_state.fetcher = None
    if 'intelligence' not in st.session_state:
        st.session_state.intelligence = None
    if 'processing_status' not in st.session_state:
        st.session_state.processing_status = {}
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = 'cards'
    if 'show_advanced' not in st.session_state:
        st.session_state.show_advanced = True
    if 'email_patterns' not in st.session_state:
        st.session_state.email_patterns = {}
    if 'executive_summary' not in st.session_state:
        st.session_state.executive_summary = None


def load_emails():
    """Fetch emails from Gmail or mock data"""
    try:
        with st.spinner('Fetching emails...'):
            if st.session_state.fetcher is None:
                st.session_state.fetcher = GmailFetcher()
            
            emails = st.session_state.fetcher.fetch_emails(
                max_results=Config.MAX_EMAILS_PER_BATCH
            )
            st.session_state.emails = emails
            
            if emails:
                st.success(f'Successfully loaded {len(emails)} emails')
            else:
                st.warning('No emails found')
            
            return emails
    except Exception as e:
        st.error(f'Error loading emails: {str(e)}')
        return []


async def process_emails_async(emails: List[Dict]):
    """Process emails with AI intelligence"""
    if st.session_state.intelligence is None:
        st.session_state.intelligence = EmailIntelligence()
    
    results = await st.session_state.intelligence.process_batch(emails)
    
    # Combine email data with processing results
    for email, result in zip(emails, results):
        email_id = email['id']
        st.session_state.processed_emails[email_id] = {
            'email_id': email_id,
            'sender': email['sender'],
            'sender_name': email['sender_name'],
            'subject': email['subject'],
            'body': email['body'],
            'snippet': email.get('snippet', ''),
            'timestamp': email['timestamp'],
            'labels': email.get('labels', []),
            'summary': result['summary'],
            'intent': result['intent'],
            'urgency': result['urgency'],
            'sentiment': result['sentiment'],
            'suggested_replies': result['suggested_replies'],
            'selected_action': None,
            'drafted_reply': '',
            'processed_at': datetime.now()
        }
        st.session_state.processing_status[email_id] = 'processed'


def process_emails():
    """Wrapper to run async email processing"""
    try:
        with st.spinner('Processing emails with AI...'):
            asyncio.run(process_emails_async(st.session_state.emails))
        st.success('Email processing complete!')
    except Exception as e:
        st.error(f'Error processing emails: {str(e)}')


def filter_emails(emails: List[Dict]) -> List[Dict]:
    """Filter emails based on selected criteria"""
    filtered = []
    
    for email_id, email_data in emails.items():
        # Filter by urgency
        if st.session_state.filter_urgency != 'All':
            if email_data.get('urgency') != st.session_state.filter_urgency:
                continue
        
        # Filter by intent
        if st.session_state.filter_intent != 'All':
            if email_data.get('intent') != st.session_state.filter_intent:
                continue
        
        filtered.append(email_data)
    
    return filtered


def display_statistics():
    """Display email statistics dashboard"""
    if not st.session_state.processed_emails:
        st.info('No processed emails to display statistics')
        return
    
    stats = CSVExporter.generate_statistics(
        list(st.session_state.processed_emails.values())
    )
    
    st.subheader('📊 Email Statistics')
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric('Total Emails', stats['total_emails'])
    
    with col2:
        processed = stats['processed_count']
        st.metric('Processed', processed)
    
    with col3:
        high_urgency = stats['by_urgency'].get('High', 0)
        st.metric('High Urgency', high_urgency)
    
    with col4:
        action_required = stats['by_intent'].get('Action Required', 0)
        st.metric('Action Required', action_required)
    
    # Detailed breakdowns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write('**By Intent**')
        if stats['by_intent']:
            st.table(stats['by_intent'])
    
    with col2:
        st.write('**By Urgency**')
        if stats['by_urgency']:
            st.table(stats['by_urgency'])
    
    with col3:
        st.write('**By Sentiment**')
        if stats['by_sentiment']:
            st.table(stats['by_sentiment'])


def display_email_list():
    """Display list of emails in sidebar"""
    st.sidebar.title('📬 Inbox')
    
    if not st.session_state.processed_emails:
        st.sidebar.info('No emails loaded. Click "Fetch Emails" to start.')
        return
    
    # Filter controls
    st.sidebar.subheader('🔍 Filters')
    
    st.session_state.filter_urgency = st.sidebar.selectbox(
        'Urgency',
        ['All'] + Config.URGENCY_LEVELS
    )
    
    st.session_state.filter_intent = st.sidebar.selectbox(
        'Intent',
        ['All'] + Config.INTENT_CATEGORIES
    )
    
    # Get filtered emails
    filtered_emails = filter_emails(st.session_state.processed_emails)
    
    st.sidebar.write(f'**{len(filtered_emails)} emails**')
    
    # Display email list
    for email in filtered_emails:
        urgency_class = f"urgency-{email['urgency'].lower()}"
        
        # Email card
        with st.sidebar.container():
            col1, col2 = st.sidebar.columns([3, 1])
            
            with col1:
                if st.sidebar.button(
                    f"📧 {email['sender_name'][:20]}",
                    key=f"email_{email['email_id']}",
                    use_container_width=True
                ):
                    st.session_state.selected_email_id = email['email_id']
                    st.rerun()
            
            with col2:
                urgency_emoji = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
                st.sidebar.write(urgency_emoji.get(email['urgency'], '⚪'))
            
            st.sidebar.caption(email['subject'][:40] + ('...' if len(email['subject']) > 40 else ''))
            st.sidebar.divider()


def display_email_details():
    """Display selected email details with advanced intelligence"""
    if not st.session_state.selected_email_id:
        st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h2>👈 Select an email to analyze</h2>
            <p>View summaries, extract insights, and get smart replies</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    email = st.session_state.processed_emails.get(st.session_state.selected_email_id)
    
    if not email:
        st.error('Email not found')
        return
    
    # Get advanced patterns if available
    patterns = st.session_state.email_patterns.get(st.session_state.selected_email_id, {})
    
    # Email header with enhanced styling
    urgency_class = f"urgency-{email['urgency'].lower()}"
    st.markdown(f"""
    <div class="email-card {urgency_class}">
        <h2>📧 {email['subject']}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write(f"**From:** {email['sender_name']}")
        if patterns and 'relationship' in patterns:
            st.caption(patterns['relationship'])
    
    with col2:
        st.write(f"**Date:** {email['timestamp'].strftime('%b %d, %H:%M')}")
        if patterns and 'pattern' in patterns:
            st.caption(f"📖 {patterns['pattern']['estimated_read_time']}")
    
    with col3:
        urgency_emoji = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
        st.write(f"**Priority:** {urgency_emoji[email['urgency']]} {email['urgency']}")
        if patterns and 'response_prediction' in patterns:
            pred = patterns['response_prediction']
            st.caption(f"⏱️ {pred['recommended_response_hours']:.0f}hr deadline")
    
    with col4:
        if patterns and 'category' in patterns:
            st.write(f"**Category:** {patterns['category']}")
        st.write(f"**Intent:** `{email['intent']}`")
    
    st.divider()
    
    # Advanced Insights Section (if patterns available)
    if patterns:
        with st.expander('🔍 Advanced Intelligence', expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                if 'pattern' in patterns:
                    pattern = patterns['pattern']
                    st.markdown('**Communication Style**')
                    st.progress(pattern['formality_score'] / 100, text=f"Formality: {pattern['formality_level'].title()}")
                    
                    st.markdown(f"""
                    <div style="margin-top: 10px;">
                        <span class="pattern-badge" style="background: #e3f2fd; color: #1976d2;">
                            {pattern['emotion'].title()}
                        </span>
                        <span class="pattern-badge" style="background: #f3e5f5; color: #7b1fa2;">
                            {pattern['communication_pace'].title()}
                        </span>
                        <span class="pattern-badge" style="background: #e8f5e9; color: #388e3c;">
                            {pattern['reading_difficulty'].title()}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.caption(f"Word count: {pattern['word_count']} | Complexity: {pattern['complexity_score']}/100")
            
            with col2:
                if 'entities' in patterns:
                    entities = patterns['entities']
                    st.markdown('**Extracted Entities**')
                    
                    if entities['dates']:
                        st.markdown('📅 **Dates:**')
                        for date in entities['dates']:
                            st.caption(f"  • {date}")
                    
                    if entities['monetary_amounts']:
                        st.markdown('💰 **Amounts:**')
                        for amount in entities['monetary_amounts']:
                            st.caption(f"  • {amount}")
                    
                    if entities['action_items']:
                        st.markdown('✅ **Actions Required:**')
                        for action in entities['action_items']:
                            st.markdown(f'<span class="entity-tag">{action}</span>', unsafe_allow_html=True)
                    
                    if entities['has_attachments']:
                        st.markdown('📎 **Contains attachments**')
            
            # Response time prediction
            if 'response_prediction' in patterns:
                pred = patterns['response_prediction']
                st.markdown('---')
                st.markdown('**⏱️ Response Time Intelligence**')
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric('Priority Score', f"{pred['priority_score']}/100")
                with col2:
                    st.metric('Recommended Response', f"{pred['recommended_response_hours']:.1f} hours")
                with col3:
                    st.metric('Deadline', pred['deadline'].split()[1])
                
                # Priority indicator
                priority_color = '#ff6b6b' if pred['priority_score'] > 70 else '#ffd93d' if pred['priority_score'] > 40 else '#51cf66'
                st.markdown(f"""
                <div class="risk-indicator">
                    <div class="risk-fill" style="width: {pred['priority_score']}%; background: {priority_color};"></div>
                </div>
                """, unsafe_allow_html=True)
                st.caption(f"Urgency Label: {pred['urgency_label']}")
    
    st.divider()
    
    # Summary Section
    st.subheader('📝 AI-Generated Summary')
    st.info(email['summary'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"**Sentiment:** {email['sentiment'].title()}")
    with col2:
        st.caption(f"**Confidence:** High")
    
    # Original email body
    with st.expander('📄 View Full Email'):
        st.text_area(
            'Email Body',
            email['body'],
            height=300,
            disabled=True,
            key=f"body_{email['email_id']}"
        )
    
    st.divider()
    
    # Smart Replies Section
    st.subheader('💬 Smart Reply Generator')
    
    reply_tabs = st.tabs(['✨ AI Suggestions', '✍️ Custom Reply', '📋 Reply History'])
    
    with reply_tabs[0]:
        st.caption('Tone-aware responses tailored to the email context')
        
        for i, reply in enumerate(email['suggested_replies']):
            tone = ['Professional', 'Friendly', 'Brief'][i] if i < 3 else 'Default'
            
            with st.container():
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 10px 0;">
                        <strong style="color: #667eea;">Option {i+1}: {tone}</strong>
                        <p style="margin-top: 8px;">{reply}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button(
                        '✓ Use',
                        key=f"reply_{email['email_id']}_{i}",
                        type='primary',
                        use_container_width=True
                    ):
                        email['selected_action'] = f'{tone} Reply'
                        email['drafted_reply'] = reply
                        st.success(f'{tone} reply selected!')
                        st.rerun()
    
    with reply_tabs[1]:
        st.write('**Craft your own personalized response:**')
        custom_reply = st.text_area(
            'Your Reply',
            height=150,
            placeholder='Type your custom reply here...',
            key=f"custom_{email['email_id']}"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button('💾 Save Custom Reply', key=f"custom_btn_{email['email_id']}", use_container_width=True):
                if custom_reply:
                    email['selected_action'] = 'Custom Reply'
                    email['drafted_reply'] = custom_reply
                    st.success('✅ Custom reply saved!')
                    st.rerun()
                else:
                    st.warning('Please enter a reply')
        
        with col2:
            if st.button('🔄 Clear', key=f"clear_custom_{email['email_id']}", use_container_width=True):
                st.rerun()
    
    with reply_tabs[2]:
        # Show drafted reply if exists
        if email.get('drafted_reply'):
            st.success('**✅ Prepared Reply:**')
            st.markdown(f"""
            <div style="background: #e8f5e9; padding: 15px; border-radius: 10px; border-left: 4px solid #4caf50;">
                <strong>Selected: {email.get('selected_action', 'Reply')}</strong>
                <p style="margin-top: 10px;">{email['drafted_reply']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button('📤 Send Email', key=f"send_{email['email_id']}", use_container_width=True, type='primary'):
                    st.success('✅ Email sent! (Mock mode)')
            
            with col2:
                if st.button('🗑️ Discard', key=f"clear_{email['email_id']}", use_container_width=True):
                    email['selected_action'] = None
                    email['drafted_reply'] = ''
                    st.rerun()
        else:
            st.info('No reply prepared yet. Select a suggested reply or write a custom one.')


def main():
    """Main application - Neural Email Intelligence Platform"""
    
    # Initialize
    init_session_state()
    Config.validate()
    
    # Enhanced Header
    st.markdown('<div class="main-header">🧠 MailMind Neural Intelligence</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="tagline">Transform your inbox into an actionable decision layer • Extract insights • Predict patterns • Respond intelligently</p>',
        unsafe_allow_html=True
    )
    
    # Control Panel
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button('📥 Fetch Emails', use_container_width=True, type='primary'):
            load_emails()
    
    with col2:
        if st.button('� Process Intelligence', use_container_width=True):
            if st.session_state.emails:
                process_emails()
                # Generate advanced insights
                generate_advanced_insights()
            else:
                st.warning('Please fetch emails first')
    
    with col3:
        view_mode = st.selectbox('📊 View', ['Dashboard', 'Cards', 'List', 'Analytics'], key='view_selector')
    
    with col4:
        if st.button('📋 Export Data', use_container_width=True):
            if st.session_state.processed_emails:
                csv_data, filename = CSVExporter.export_to_csv(
                    list(st.session_state.processed_emails.values())
                )
                st.download_button(
                    label='⬇️ Download CSV',
                    data=csv_data,
                    file_name=filename,
                    mime='text/csv',
                    use_container_width=True
                )
            else:
                st.warning('No processed emails to export')
    
    st.divider()
    
    # Display Executive Dashboard if emails are processed
    if st.session_state.processed_emails and view_mode == 'Dashboard':
        display_executive_dashboard()
        st.divider()
    
    # Display content based on view mode
    if view_mode == 'Analytics':
        display_advanced_analytics()
    else:
        # Main layout - Email list and details
        display_email_list()
        display_email_details()
    
    # Footer with enhanced info
    st.sidebar.divider()
    st.sidebar.markdown('### 🎯 Quick Stats')
    if st.session_state.emails:
        st.sidebar.metric('Total Emails', len(st.session_state.emails))
        st.sidebar.metric('Processed', len(st.session_state.processed_emails))
        if st.session_state.executive_summary:
            summary = st.session_state.executive_summary
            st.sidebar.metric('Workload Level', summary.get('workload_level', 'N/A'))
            st.sidebar.metric('Risk Score', f"{summary.get('risk_score', 0)}/100")
    
    st.sidebar.divider()
    st.sidebar.caption(
        f'Mode: {"🎭 Mock Data" if Config.USE_MOCK_DATA else "📬 Gmail API"}'
    )
    st.sidebar.caption('MailMind Neural v2.0 - Advanced Email Intelligence')


def generate_advanced_insights():
    """Generate advanced pattern analysis and insights"""
    if not st.session_state.processed_emails:
        return
    
    emails_list = list(st.session_state.processed_emails.values())
    
    # Generate executive summary
    st.session_state.executive_summary = EmailInsightGenerator.generate_executive_summary(emails_list)
    
    # Analyze patterns for each email
    for email_id, email in st.session_state.processed_emails.items():
        pattern = EmailPatternAnalyzer.detect_communication_style(email)
        entities = EmailPatternAnalyzer.extract_entities(email)
        response_time = EmailPatternAnalyzer.predict_response_time(email)
        category = SmartCategorizer.detect_email_category(email)
        relationship = SmartCategorizer.detect_sender_relationship(email)
        
        st.session_state.email_patterns[email_id] = {
            'pattern': pattern,
            'entities': entities,
            'response_prediction': response_time,
            'category': category,
            'relationship': relationship
        }


def display_executive_dashboard():
    """Display executive-level insights dashboard"""
    if not st.session_state.executive_summary:
        return
    
    summary = st.session_state.executive_summary
    
    st.markdown('### 🎯 Executive Command Center')
    
    # Top metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric('Total Emails', summary['total_emails'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric('High Priority', summary['high_priority_count'], 
                 delta=f"{summary['action_required_count']} need action")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        workload_color = '🔴' if summary['workload_score'] > 70 else '🟡' if summary['workload_score'] > 40 else '🟢'
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric('Workload', f"{workload_color} {summary['workload_level']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        risk_color = '🔴' if summary['risk_score'] > 60 else '🟡' if summary['risk_score'] > 30 else '🟢'
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric('Risk Level', f"{risk_color} {summary['risk_level']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric('Processing Time', f"~{summary['estimated_processing_minutes']} min")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Strategic recommendation
    st.markdown(f"""
    <div class="insight-card">
        <h4>📋 Strategic Recommendation</h4>
        <p style="font-size: 1.1rem; margin: 0;">{summary['recommendation']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Risk and workload visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('#### ⚡ Workload Analysis')
        st.progress(summary['workload_score'] / 100)
        st.caption(f"Score: {summary['workload_score']}/100")
    
    with col2:
        st.markdown('#### ⚠️ Risk Assessment')
        st.progress(summary['risk_score'] / 100)
        st.caption(f"Score: {summary['risk_score']}/100")


def display_advanced_analytics():
    """Display advanced analytics view"""
    st.markdown('### 📊 Advanced Analytics & Insights')
    
    if not st.session_state.email_patterns:
        st.info('Process emails first to see advanced analytics')
        return
    
    # Communication style distribution
    st.markdown('#### 🎨 Communication Patterns')
    
    formality_scores = []
    emotion_distribution = {}
    categories = {}
    relationships = {}
    
    for email_id, data in st.session_state.email_patterns.items():
        pattern = data['pattern']
        formality_scores.append(pattern['formality_score'])
        
        emotion = pattern['emotion']
        emotion_distribution[emotion] = emotion_distribution.get(emotion, 0) + 1
        
        category = data['category']
        categories[category] = categories.get(category, 0) + 1
        
        relationship = data['relationship']
        relationships[relationship] = relationships.get(relationship, 0) + 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('**Formality Distribution**')
        avg_formality = sum(formality_scores) / len(formality_scores) if formality_scores else 0
        st.metric('Average Formality', f"{int(avg_formality)}/100")
        st.progress(avg_formality / 100)
        
        st.markdown('**Emotional Tone**')
        for emotion, count in sorted(emotion_distribution.items(), key=lambda x: x[1], reverse=True):
            st.write(f"{emotion.title()}: {count} emails")
    
    with col2:
        st.markdown('**Email Categories**')
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            st.write(f"{category}: {count}")
        
        st.markdown('**Sender Relationships**')
        for rel, count in sorted(relationships.items(), key=lambda x: x[1], reverse=True):
            st.write(f"{rel}: {count}")
    
    # Entity extraction summary
    st.markdown('#### 🔍 Extracted Entities Across All Emails')
    
    all_dates = []
    all_amounts = []
    all_actions = []
    
    for data in st.session_state.email_patterns.values():
        entities = data['entities']
        all_dates.extend(entities['dates'])
        all_amounts.extend(entities['monetary_amounts'])
        all_actions.extend(entities['action_items'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric('📅 Dates Found', len(all_dates))
        if all_dates[:3]:
            for date in all_dates[:3]:
                st.caption(f"• {date}")
    
    with col2:
        st.metric('� Money Mentions', len(all_amounts))
        if all_amounts[:3]:
            for amount in all_amounts[:3]:
                st.caption(f"• {amount}")
    
    with col3:
        st.metric('✅ Action Items', len(set(all_actions)))
        action_count = {}
        for action in all_actions:
            action_count[action] = action_count.get(action, 0) + 1
        for action, count in sorted(action_count.items(), key=lambda x: x[1], reverse=True)[:3]:
            st.caption(f"• {action.title()} ({count}x)")
    
    # Response time predictions
    st.markdown('#### ⏱️ Response Time Intelligence')
    
    urgent_count = 0
    overdue_risk = 0
    
    for data in st.session_state.email_patterns.values():
        pred = data['response_prediction']
        if pred['recommended_response_hours'] <= 2:
            urgent_count += 1
        if pred['priority_score'] > 80:
            overdue_risk += 1
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('🔥 Urgent (< 2hr)', urgent_count)
    with col2:
        st.metric('⚠️ High Priority', overdue_risk)
    with col3:
        avg_hours = sum(data['response_prediction']['recommended_response_hours'] 
                       for data in st.session_state.email_patterns.values()) / len(st.session_state.email_patterns)
        st.metric('📊 Avg Response Time', f"{avg_hours:.1f} hrs")


if __name__ == '__main__':
    main()

