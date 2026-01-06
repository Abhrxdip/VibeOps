"""
MailMind Test Suite
Quick tests to verify functionality
"""

import sys
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        import streamlit
        import pandas
        import openai
        from dotenv import load_dotenv
        print("✓ All core imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    try:
        from config import Config
        Config.validate()
        print(f"✓ Configuration loaded")
        print(f"  - Mock mode: {Config.USE_MOCK_DATA}")
        print(f"  - Max emails: {Config.MAX_EMAILS_PER_BATCH}")
        print(f"  - AI fallback: {Config.ENABLE_AI_FALLBACK}")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False


def test_mock_data():
    """Test mock data generation"""
    print("\nTesting mock data...")
    try:
        from mock_data import MockEmailGenerator
        emails = MockEmailGenerator.get_mock_emails(5)
        print(f"✓ Mock data generated: {len(emails)} emails")
        print(f"  - Sample subject: {emails[0]['subject']}")
        return True
    except Exception as e:
        print(f"✗ Mock data error: {e}")
        return False


def test_gmail_fetcher():
    """Test Gmail fetcher in mock mode"""
    print("\nTesting Gmail fetcher...")
    try:
        from gmail_fetcher import GmailFetcher
        fetcher = GmailFetcher(use_mock=True)
        emails = fetcher.fetch_emails(max_results=3)
        print(f"✓ Gmail fetcher working: {len(emails)} emails fetched")
        return True
    except Exception as e:
        print(f"✗ Gmail fetcher error: {e}")
        return False


def test_email_intelligence():
    """Test email intelligence module"""
    print("\nTesting email intelligence...")
    try:
        from email_intelligence import EmailIntelligence
        intelligence = EmailIntelligence()
        
        test_email = {
            'id': 'test_001',
            'sender': 'test@example.com',
            'sender_name': 'Test User',
            'subject': 'Urgent: Meeting Request',
            'body': 'We need to schedule an urgent meeting to discuss the project.',
            'timestamp': datetime.now()
        }
        
        result = intelligence._rule_based_process_email(test_email)
        print(f"✓ Email intelligence working")
        print(f"  - Intent: {result['intent']}")
        print(f"  - Urgency: {result['urgency']}")
        print(f"  - Sentiment: {result['sentiment']}")
        return True
    except Exception as e:
        print(f"✗ Email intelligence error: {e}")
        return False


def test_csv_export():
    """Test CSV export functionality"""
    print("\nTesting CSV export...")
    try:
        from csv_exporter import CSVExporter
        
        test_data = [{
            'email_id': 'test_001',
            'sender': 'test@example.com',
            'sender_name': 'Test User',
            'subject': 'Test Email',
            'timestamp': datetime.now(),
            'summary': 'This is a test summary',
            'intent': 'Informational',
            'urgency': 'Low',
            'sentiment': 'Neutral',
            'selected_action': 'None',
            'drafted_reply': '',
            'processed_at': datetime.now()
        }]
        
        csv_string, filename = CSVExporter.export_to_csv(test_data)
        print(f"✓ CSV export working")
        print(f"  - Filename: {filename}")
        print(f"  - Size: {len(csv_string)} bytes")
        return True
    except Exception as e:
        print(f"✗ CSV export error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("MailMind Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_mock_data,
        test_gmail_fetcher,
        test_email_intelligence,
        test_csv_export
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Test Results: {passed}/{total} passed")
    print("=" * 50)
    
    if passed == total:
        print("\n✓ All tests passed! MailMind is ready to use.")
        print("  Run: streamlit run app.py")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
