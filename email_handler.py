"""
Email Handler Module
Manages temporary email accounts for verification purposes
"""

import requests
import json
import time
from typing import Dict, Optional, List
from urllib.parse import urlencode


class EmailHandler:
    def __init__(self, config_path: str = "config/email_config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.service = self.config['service']
        self.session = requests.Session()
        self.email_address = None
        self.token = None
        self.check_interval = 10  # seconds
        self.max_wait_time = self.config.get('verification_timeout', 300)  # 5 minutes
    
    def create_temp_email(self) -> Optional[Dict[str, str]]:
        """Create a new temporary email address"""
        if self.service == 'guerrilla_mail':
            return self._create_guerrilla_email()
        elif self.service == 'temp_mail':
            return self._create_temp_mail_email()
        else:
            raise ValueError(f"Unsupported email service: {self.service}")
    
    def check_inbox(self) -> List[Dict]:
        """Check the temporary email inbox for new messages"""
        if self.service == 'guerrilla_mail':
            return self._check_guerrilla_inbox()
        elif self.service == 'temp_mail':
            return self._check_temp_mail_inbox()
        else:
            raise ValueError(f"Unsupported email service: {self.service}")
    
    def wait_for_verification_email(self, subject_keywords: List[str], 
                                  sender_filter: Optional[str] = None) -> Optional[Dict]:
        """Wait for a verification email with specific subject keywords"""
        start_time = time.time()
        
        while time.time() - start_time < self.max_wait_time:
            emails = self.check_inbox()
            
            for email in emails:
                # Check subject for keywords
                subject_match = any(keyword.lower() in email.get('subject', '').lower() 
                                  for keyword in subject_keywords)
                
                # Check sender if specified
                sender_match = True
                if sender_filter:
                    sender_match = sender_filter.lower() in email.get('sender', '').lower()
                
                if subject_match and sender_match:
                    return email
            
            # Wait before checking again
            time.sleep(self.check_interval)
        
        return None
    
    def extract_verification_link(self, email_content: str) -> Optional[str]:
        """Extract verification link from email content"""
        import re
        
        # Look for URLs in the email content
        url_pattern = r'https?://[^\s\'"]+'
        urls = re.findall(url_pattern, email_content)
        
        # Filter for likely verification links
        verification_patterns = [
            r'verify',
            r'confirm',
            r'activate',
            r'email',
            r'token',
            r'auth'
        ]
        
        for url in urls:
            if any(pattern in url.lower() for pattern in verification_patterns):
                return url
        
        # If no pattern-matching URLs, return the first URL as fallback
        return urls[0] if urls else None
    
    def _create_guerrilla_email(self) -> Optional[Dict[str, str]]:
        """Create a temporary email using Guerrilla Mail"""
        url = self.config['api_base_url']
        params = {
            'f': 'get_email_address',
            'lang': 'en'
        }
        
        try:
            response = self.session.get(url, params=params)
            data = response.json()
            
            if 'email_addr' in data:
                self.email_address = data['email_addr']
                self.token = data.get('sid_token')
                
                return {
                    'email': self.email_address,
                    'token': self.token
                }
        except Exception as e:
            print(f"Error creating Guerrilla Mail address: {e}")
        
        return None
    
    def _check_guerrilla_inbox(self) -> List[Dict]:
        """Check Guerrilla Mail inbox"""
        if not self.token:
            print("No active Guerrilla Mail session")
            return []
        
        url = self.config['api_base_url']
        params = {
            'f': 'check_email',
            'sid_token': self.token,
            'seq': '0'
        }
        
        try:
            response = self.session.get(url, params=params)
            data = response.json()
            
            emails = []
            if 'list' in data:
                for email_data in data['list']:
                    email_info = {
                        'id': email_data.get('mail_id'),
                        'subject': email_data.get('mail_subject', ''),
                        'sender': email_data.get('mail_from', ''),
                        'date': email_data.get('mail_timestamp', ''),
                        'content': self._get_guerrilla_email_content(email_data.get('mail_id'))
                    }
                    emails.append(email_info)
            
            return emails
        except Exception as e:
            print(f"Error checking Guerrilla Mail inbox: {e}")
            return []
    
    def _get_guerrilla_email_content(self, email_id: str) -> str:
        """Get the content of a specific email"""
        if not self.token:
            return ""
        
        url = self.config['api_base_url']
        params = {
            'f': 'fetch_email',
            'sid_token': self.token,
            'email_id': email_id
        }
        
        try:
            response = self.session.get(url, params=params)
            data = response.json()
            return data.get('mail_body', '')
        except Exception as e:
            print(f"Error getting email content: {e}")
            return ""
    
    def _create_temp_mail_email(self) -> Optional[Dict[str, str]]:
        """Create a temporary email using Temp Mail service"""
        # Placeholder implementation - actual API details would be needed
        print("Temp Mail implementation needed")
        return None
    
    def _check_temp_mail_inbox(self) -> List[Dict]:
        """Check Temp Mail inbox"""
        # Placeholder implementation
        print("Temp Mail inbox check implementation needed")
        return []
    
    def get_email_address(self) -> Optional[str]:
        """Get the current temporary email address"""
        return self.email_address