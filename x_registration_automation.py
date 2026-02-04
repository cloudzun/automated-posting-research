#!/usr/bin/env python3
"""
X Account Registration Automation Script
Uses the temporary email from tmpmail to register an X account
"""

import requests
import time
import re
import subprocess
import os
from urllib.parse import urlparse, parse_qs
import json

def get_temp_email():
    """Get the temporary email address from tmpmail"""
    try:
        result = subprocess.run(['/tmp/tmpmail/tmpmail'], capture_output=True, text=True, check=True)
        email = result.stdout.strip()
        print(f"Using temporary email: {email}")
        return email
    except subprocess.CalledProcessError as e:
        print(f"Error getting temporary email: {e}")
        return None

def simulate_x_registration_flow(temp_email):
    """Simulate the X registration flow using browser automation"""
    
    print("Starting X registration process...")
    
    # Create a session with appropriate headers to mimic a real browser
    session = requests.Session()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }
    
    session.headers.update(headers)
    
    # Try to access X signup page
    try:
        print("Accessing X signup page...")
        response = session.get("https://x.com/i/flow/signup", allow_redirects=True)
        
        if response.status_code == 200:
            print("Successfully accessed X signup page")
            
            # Look for CSRF tokens or other hidden fields required for the form
            # This is a simplified representation - actual implementation would be more complex
            csrf_token_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
            if csrf_token_match:
                csrf_token = csrf_token_match.group(1)
                print("Found CSRF token")
            else:
                print("CSRF token not found, but continuing...")
                csrf_token = ""
            
            # At this point, we would need to handle the registration form
            # However, X has sophisticated anti-bot measures including:
            # - CAPTCHA challenges
            # - Phone/email verification
            # - Behavioral analysis
            # - Rate limiting
            
            print("Attempting to submit registration form...")
            
            # This is where the automation would fail due to X's security measures
            # X registration typically requires:
            # 1. Solving CAPTCHA
            # 2. Email verification (which we can potentially handle)
            # 3. Additional verification steps
            
            # Let's try to initiate the signup flow with the email
            signup_payload = {
                "flow_name": "signup",
                "input_flow_data": {
                    "flow_context": {
                        "debug_overrides": {},
                        "start_location": {
                            "location": "unknown"
                        }
                    },
                    "metadata": {
                        "initiating_source": "unknown",
                        "entry_point": "email"
                    }
                }
            }
            
            # Try to start the signup flow
            flow_response = session.post(
                "https://x.com/i/api/1.1/onboarding/task.json",
                json=signup_payload,
                headers={
                    'User-Agent': headers['User-Agent'],
                    'Accept': '*/*',
                    'Content-Type': 'application/json',
                    'X-Twitter-Auth-Type': 'OAuth2Session',
                    'X-Twitter-Active-User': 'yes',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Referer': 'https://x.com/i/flow/signup',
                }
            )
            
            if flow_response.status_code == 200:
                print("Successfully initiated signup flow")
                print("Response received, processing tasks...")
                
                # Process the flow response
                try:
                    flow_data = flow_response.json()
                    
                    # Look for tasks in the response
                    if 'subtasks' in flow_data or 'flow_token' in flow_data:
                        print("Signup flow initiated successfully")
                        
                        # In a real implementation, we would need to handle each step:
                        # 1. Enter email
                        # 2. Handle CAPTCHA (this is the hardest part)
                        # 3. Verify email
                        # 4. Set username/password
                        # 5. Complete profile
                        
                        print("Note: Actual X registration would require solving CAPTCHAs and other anti-bot measures")
                        return True
                    else:
                        print("Unexpected response structure")
                        return False
                        
                except json.JSONDecodeError:
                    print("Could not decode JSON response")
                    return False
            else:
                print(f"Failed to initiate signup flow: {flow_response.status_code}")
                print(f"Response: {flow_response.text[:500]}")
                return False
                
        else:
            print(f"Failed to access X signup page: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return False

def main():
    print("Starting X account registration automation...")
    
    # Get temporary email
    temp_email = get_temp_email()
    
    if not temp_email:
        print("Failed to get temporary email")
        return False
    
    print(f"Got temporary email: {temp_email}")
    
    # Attempt X registration
    success = simulate_x_registration_flow(temp_email)
    
    if success:
        print("\nX registration process initiated successfully!")
        print("Note: Due to X's anti-bot measures, full automation is challenging.")
        print("The process would require manual intervention for CAPTCHA solving.")
    else:
        print("\nFailed to initiate X registration.")
    
    return success

if __name__ == "__main__":
    main()