"""
CAPTCHA Solver Module
Handles various types of CAPTCHA solving through third-party services
"""

import requests
import time
import json
from typing import Dict, Optional
from io import BytesIO


class CaptchaSolver:
    def __init__(self, config_path: str = "config/captcha_config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.service = self.config['service']
        self.api_key = self.config['api_key']
        self.timeout = self.config.get('timeout', 120)
        self.retry_attempts = self.config.get('retry_attempts', 3)
    
    def solve_image_captcha(self, image_data: bytes) -> Optional[str]:
        """Solve image-based CAPTCHA"""
        if self.service == '2captcha':
            return self._solve_with_2captcha(image_data)
        elif self.service == 'anti_captcha':
            return self._solve_with_antibotcaptcha(image_data)
        else:
            raise ValueError(f"Unsupported CAPTCHA service: {self.service}")
    
    def solve_recaptcha_v2(self, site_key: str, page_url: str) -> Optional[str]:
        """Solve reCAPTCHA v2"""
        if self.service == '2captcha':
            return self._solve_recaptcha_v2_2captcha(site_key, page_url)
        elif self.service == 'anti_captcha':
            return self._solve_recaptcha_v2_antibotcaptcha(site_key, page_url)
        else:
            raise ValueError(f"Unsupported CAPTCHA service: {self.service}")
    
    def solve_recaptcha_v3(self, site_key: str, page_url: str, action: str = 'verify') -> Optional[str]:
        """Solve reCAPTCHA v3"""
        if self.service == '2captcha':
            return self._solve_recaptcha_v3_2captcha(site_key, page_url, action)
        else:
            raise ValueError(f"reCAPTCHA v3 not supported by {self.service}")
    
    def _solve_with_2captcha(self, image_data: bytes) -> Optional[str]:
        """Solve CAPTCHA using 2captcha service"""
        # Upload image to 2captcha
        upload_url = "https://2captcha.com/in.php"
        
        files = {'file': ('captcha.jpg', image_data, 'image/jpeg')}
        data = {
            'key': self.api_key,
            'method': 'post',
            'json': 1
        }
        
        try:
            response = requests.post(upload_url, files=files, data=data)
            result = response.json()
            
            if result['status'] != 1:
                print(f"Error uploading CAPTCHA: {result}")
                return None
            
            captcha_id = result['request']
            
            # Poll for solution
            fetch_url = "https://2captcha.com/res.php"
            for _ in range(int(self.timeout / 5)):
                time.sleep(5)
                params = {
                    'key': self.api_key,
                    'action': 'get',
                    'id': captcha_id,
                    'json': 1
                }
                
                response = requests.get(fetch_url, params=params)
                result = response.json()
                
                if result['status'] == 1:
                    return result['request']
                elif result['request'] != 'CAPCHA_NOT_READY':
                    print(f"CAPTCHA solving error: {result}")
                    break
        except Exception as e:
            print(f"Error solving CAPTCHA with 2captcha: {e}")
        
        return None
    
    def _solve_recaptcha_v2_2captcha(self, site_key: str, page_url: str) -> Optional[str]:
        """Solve reCAPTCHA v2 using 2captcha"""
        url = "https://2captcha.com/in.php"
        
        data = {
            'key': self.api_key,
            'method': 'userrecaptcha',
            'googlekey': site_key,
            'pageurl': page_url,
            'json': 1
        }
        
        try:
            response = requests.post(url, data=data)
            result = response.json()
            
            if result['status'] != 1:
                print(f"Error submitting reCAPTCHA: {result}")
                return None
            
            captcha_id = result['request']
            
            # Poll for solution
            fetch_url = "https://2captcha.com/res.php"
            for _ in range(int(self.timeout / 5)):
                time.sleep(5)
                params = {
                    'key': self.api_key,
                    'action': 'get',
                    'id': captcha_id,
                    'json': 1
                }
                
                response = requests.get(fetch_url, params=params)
                result = response.json()
                
                if result['status'] == 1:
                    return result['request']
                elif result['request'] != 'CAPCHA_NOT_READY':
                    print(f"reCAPTCHA solving error: {result}")
                    break
        except Exception as e:
            print(f"Error solving reCAPTCHA with 2captcha: {e}")
        
        return None
    
    def _solve_recaptcha_v3_2captcha(self, site_key: str, page_url: str, action: str) -> Optional[str]:
        """Solve reCAPTCHA v3 using 2captcha"""
        url = "https://2captcha.com/in.php"
        
        data = {
            'key': self.api_key,
            'method': 'userrecaptcha',
            'version': 'v3',
            'googlekey': site_key,
            'pageurl': page_url,
            'action': action,
            'json': 1
        }
        
        try:
            response = requests.post(url, data=data)
            result = response.json()
            
            if result['status'] != 1:
                print(f"Error submitting reCAPTCHA v3: {result}")
                return None
            
            captcha_id = result['request']
            
            # Poll for solution
            fetch_url = "https://2captcha.com/res.php"
            for _ in range(int(self.timeout / 5)):
                time.sleep(5)
                params = {
                    'key': self.api_key,
                    'action': 'get',
                    'id': captcha_id,
                    'json': 1
                }
                
                response = requests.get(fetch_url, params=params)
                result = response.json()
                
                if result['status'] == 1:
                    return result['request']
                elif result['request'] != 'CAPCHA_NOT_READY':
                    print(f"reCAPTCHA v3 solving error: {result}")
                    break
        except Exception as e:
            print(f"Error solving reCAPTCHA v3 with 2captcha: {e}")
        
        return None
    
    def _solve_with_antibotcaptcha(self, image_data: bytes) -> Optional[str]:
        """Solve CAPTCHA using Anti-Captcha service"""
        # Implementation for Anti-Captcha service
        # This is a placeholder - actual implementation would require
        # the Anti-Captcha API details
        print("Anti-Captcha implementation needed")
        return None
    
    def _solve_recaptcha_v2_antibotcaptcha(self, site_key: str, page_url: str) -> Optional[str]:
        """Solve reCAPTCHA v2 using Anti-Captcha service"""
        # Implementation for Anti-Captcha reCAPTCHA solving
        print("Anti-Captcha reCAPTCHA v2 implementation needed")
        return None