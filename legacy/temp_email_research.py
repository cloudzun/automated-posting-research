#!/usr/bin/env python3
"""
Research temporary email services that can be used programmatically
"""

import requests
import time
import re
import json
from urllib.parse import urlparse

def test_temp_email_services():
    """Test various temporary email services for API accessibility"""
    
    services = [
        {
            "name": "10MinuteMail",
            "url": "https://www.10minutemail.com/",
            "email_endpoint": "https://www.10minutemail.com/session/address",
            "method": "GET"
        },
        {
            "name": "TempMail",
            "url": "https://temp-mail.org",
            "email_endpoint": "https://api.temp-mail.org/request/mail/id/",
            "method": "GET"
        },
        {
            "name": "DisposableMail",
            "url": "https://www.disposablemail.com/",
            "email_endpoint": "https://www.disposablemail.com/api/mailbox",
            "method": "POST"
        }
    ]
    
    results = []
    
    for service in services:
        try:
            print(f"Testing {service['name']}...")
            
            # Try to get a temporary email
            if service['method'] == 'GET':
                response = requests.get(service['email_endpoint'], timeout=10)
            else:
                response = requests.post(service['email_endpoint'], timeout=10)
                
            if response.status_code == 200:
                print(f"  Success: {response.status_code}")
                print(f"  Response: {response.text[:200]}...")
                results.append({
                    "service": service['name'],
                    "success": True,
                    "response": response.text[:500]
                })
            else:
                print(f"  Failed: {response.status_code}")
                results.append({
                    "service": service['name'],
                    "success": False,
                    "response": f"Status code: {response.status_code}"
                })
                
        except Exception as e:
            print(f"  Error: {str(e)}")
            results.append({
                "service": service['name'],
                "success": False,
                "response": str(e)
            })
        
        time.sleep(2)  # Be respectful to APIs
    
    return results

if __name__ == "__main__":
    print("Testing temporary email services for automation capability...")
    results = test_temp_email_services()
    
    print("\n--- Results ---")
    for result in results:
        status = "✓" if result['success'] else "✗"
        print(f"{status} {result['service']}: {result['response'][:100]}...")