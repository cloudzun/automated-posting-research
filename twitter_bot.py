"""
Twitter Bot Module
Main module for creating Twitter accounts and posting content
"""

import time
import re
from typing import Optional, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from modules.proxy_manager import ProxyManager
from modules.captcha_solver import CaptchaSolver
from modules.email_handler import EmailHandler


class TwitterBot:
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.captcha_solver = CaptchaSolver()
        self.email_handler = EmailHandler()
        self.driver = None
        self.wait = None
    
    def setup_driver(self, proxy: Optional[Dict] = None):
        """Setup Chrome WebDriver with proxy if provided"""
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Add proxy if provided
        if proxy:
            proxy_server = proxy.get('http') or proxy.get('https')
            if proxy_server:
                # Extract host and port from proxy string
                import re
                proxy_match = re.search(r'://([^:]+):(\d+)', proxy_server)
                if proxy_match:
                    host, port = proxy_match.groups()
                    options.add_argument(f'--proxy-server=http://{host}:{port}')
        
        # Create driver instance
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 20)
    
    def close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
    
    def create_twitter_account(self, first_name: str, last_name: str, 
                             phone_or_email: str, password: str) -> bool:
        """Create a new Twitter account"""
        try:
            # Navigate to Twitter signup page
            self.driver.get("https://twitter.com/i/flow/signup")
            time.sleep(5)
            
            # Wait for the signup form to load
            # We'll need to interact with the dynamic flow
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
            
            # Fill in the name fields
            try:
                # Find and fill first name
                name_input = self.driver.find_element(By.CSS_SELECTOR, "input[autocomplete='name']")
                name_input.clear()
                name_input.send_keys(f"{first_name} {last_name}")
            except NoSuchElementException:
                # Try alternative selectors
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                for inp in inputs:
                    if "name" in inp.get_attribute("autocomplete") or "text" in inp.get_attribute("type"):
                        inp.clear()
                        inp.send_keys(f"{first_name} {last_name}")
                        break
            
            # Click next
            next_buttons = self.driver.find_elements(By.XPATH, "//span[contains(text(), 'Next') or contains(text(), '下一步')]")
            if next_buttons:
                next_buttons[-1].click()
            else:
                # Alternative selector for next button
                next_btns = self.driver.find_elements(By.CSS_SELECTOR, "div[data-testid='ocfEnterTextNextButton'], div[role='button']")
                for btn in next_btns:
                    if "next" in btn.text.lower() or btn.get_attribute("data-testid") == "ocfEnterTextNextButton":
                        btn.click()
                        break
            
            time.sleep(3)
            
            # Now we should be at the email/phone input stage
            try:
                # Try email first
                email_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='email'], input[autocomplete*='email']")
                email_input.clear()
                email_input.send_keys(phone_or_email)
            except NoSuchElementException:
                # If no email field, try phone
                try:
                    phone_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='tel'], input[autocomplete*='tel']")
                    phone_input.clear()
                    phone_input.send_keys(phone_or_email)
                except NoSuchElementException:
                    # Look for any input field that could be for email/phone
                    inputs = self.driver.find_elements(By.TAG_NAME, "input")
                    for inp in inputs:
                        if inp.is_displayed():
                            inp.clear()
                            inp.send_keys(phone_or_email)
                            break
            
            # Click next again
            next_buttons = self.driver.find_elements(By.XPATH, "//span[contains(text(), 'Next') or contains(text(), '下一步')]")
            if next_buttons:
                next_buttons[-1].click()
            else:
                next_btns = self.driver.find_elements(By.CSS_SELECTOR, "div[data-testid='ocfEnterTextNextButton'], div[role='button']")
                for btn in next_btns:
                    if "next" in btn.text.lower() or btn.get_attribute("data-testid") == "ocfEnterTextNextButton":
                        btn.click()
                        break
            
            time.sleep(3)
            
            # Handle birthday if prompted
            try:
                month_select = self.driver.find_element(By.CSS_SELECTOR, "select[aria-label*='month'], select[name='month']")
                month_select.click()
                # Select a random month
                from selenium.webdriver.support.ui import Select
                select = Select(month_select)
                select.select_by_value("1")  # January
                
                day_select = self.driver.find_element(By.CSS_SELECTOR, "select[aria-label*='day'], select[name='day']")
                day_select.click()
                select = Select(day_select)
                select.select_by_value("15")  # Day 15th
                
                year_select = self.driver.find_element(By.CSS_SELECTOR, "select[aria-label*='year'], select[name='year']")
                year_select.click()
                select = Select(year_select)
                select.select_by_value("1990")  # Year 1990
            except NoSuchElementException:
                pass  # Birthday not required
            
            # Click next again
            next_buttons = self.driver.find_elements(By.XPATH, "//span[contains(text(), 'Next') or contains(text(), '下一步')]")
            if next_buttons:
                next_buttons[-1].click()
            else:
                next_btns = self.driver.find_elements(By.CSS_SELECTOR, "div[data-testid='ocfEnterTextNextButton'], div[role='button']")
                for btn in next_btns:
                    if "next" in btn.text.lower() or btn.get_attribute("data-testid") == "ocfEnterTextNextButton":
                        btn.click()
                        break
            
            time.sleep(5)
            
            # Set password
            try:
                password_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
                if len(password_inputs) >= 2:
                    # Usually there are two password fields: password and confirmation
                    password_inputs[0].send_keys(password)
                    password_inputs[1].send_keys(password)
                else:
                    # Only one password field
                    password_inputs[0].send_keys(password)
                
                # Click next
                next_buttons = self.driver.find_elements(By.XPATH, "//span[contains(text(), 'Next') or contains(text(), '下一步')]")
                if next_buttons:
                    next_buttons[-1].click()
                else:
                    next_btns = self.driver.find_elements(By.CSS_SELECTOR, "div[data-testid='ocfEnterTextNextButton'], div[role='button']")
                    for btn in next_btns:
                        if "next" in btn.text.lower() or btn.get_attribute("data-testid") == "ocfEnterTextNextButton":
                            btn.click()
                            break
            except NoSuchElementException:
                pass  # Password step might be skipped
            
            time.sleep(5)
            
            # Handle CAPTCHA if present
            if self._is_captcha_present():
                if not self._solve_captcha():
                    print("Failed to solve CAPTCHA")
                    return False
            
            # Wait for account verification (this might involve email verification)
            time.sleep(10)
            
            return True
            
        except Exception as e:
            print(f"Error creating Twitter account: {e}")
            return False
    
    def _is_captcha_present(self) -> bool:
        """Check if CAPTCHA is present on the page"""
        try:
            # Look for common CAPTCHA elements
            captcha_elements = self.driver.find_elements(
                By.CSS_SELECTOR, 
                ".g-recaptcha, .captcha, #captcha, [src*='captcha'], iframe[src*='captcha']"
            )
            return len(captcha_elements) > 0
        except:
            return False
    
    def _solve_captcha(self) -> bool:
        """Solve CAPTCHA on the current page"""
        try:
            # Take screenshot of CAPTCHA
            captcha_element = self.driver.find_element(By.CSS_SELECTOR, ".g-recaptcha, .captcha, #captcha, [src*='captcha']")
            
            # Get CAPTCHA image
            # For reCAPTCHA, we need to handle it differently
            if "g-recaptcha" in captcha_element.get_attribute("class"):
                # This is a reCAPTCHA - get the site key
                iframe = self.driver.find_element(By.CSS_SELECTOR, "iframe[src*='google.com/recaptcha']")
                src = iframe.get_attribute("src")
                
                # Extract site key from URL
                import urllib.parse
                parsed = urllib.parse.urlparse(src)
                params = urllib.parse.parse_qs(parsed.query)
                site_key = params.get('k', [None])[0]
                
                if site_key:
                    solution = self.captcha_solver.solve_recaptcha_v2(
                        site_key, 
                        self.driver.current_url
                    )
                    
                    if solution:
                        # Execute JavaScript to enter the solution
                        self.driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{solution}'")
                        return True
            else:
                # Regular image CAPTCHA
                captcha_screenshot = captcha_element.screenshot_as_png
                solution = self.captcha_solver.solve_image_captcha(captcha_screenshot)
                
                if solution:
                    # Find CAPTCHA input and fill it
                    captcha_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[name*='captcha'], input[placeholder*='captcha']")
                    if captcha_inputs:
                        captcha_inputs[0].send_keys(solution)
                        return True
        
        except Exception as e:
            print(f"Error solving CAPTCHA: {e}")
        
        return False
    
    def login_to_account(self, username: str, password: str) -> bool:
        """Login to an existing Twitter account"""
        try:
            self.driver.get("https://twitter.com/login")
            time.sleep(3)
            
            # Find username/email input
            username_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='text'], input[type='text']")
            username_input.send_keys(username)
            
            # Click next
            next_button = self.driver.find_element(By.CSS_SELECTOR, "div[role='button'][data-testid*='Submit']")
            next_button.click()
            time.sleep(2)
            
            # Find password input
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='password'], input[type='password']")
            password_input.send_keys(password)
            
            # Click login
            login_button = self.driver.find_element(By.CSS_SELECTOR, "div[role='button'][data-testid*='LoginForm']")
            login_button.click()
            
            # Wait for login to complete
            time.sleep(5)
            
            # Verify we're logged in by checking for elements on the home page
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='primaryColumn']")))
                return True
            except TimeoutException:
                return False
                
        except Exception as e:
            print(f"Error logging in: {e}")
            return False
    
    def post_tweet(self, content: str) -> Optional[str]:
        """Post a tweet and return the tweet URL"""
        try:
            # Wait for the tweet box to appear
            tweet_box = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']"))
            )
            
            # Clear and type the content
            tweet_box.click()
            tweet_box.clear()
            tweet_box.send_keys(content)
            
            # Wait for the tweet button to become clickable
            tweet_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tweetButtonInline']"))
            )
            
            # Click the tweet button
            tweet_button.click()
            
            # Wait for the tweet to be posted and get the URL
            time.sleep(5)
            
            # Get the tweet URL from the current page or notification
            current_url = self.driver.current_url
            if "/status/" in current_url:
                return current_url
            else:
                # Try to find the tweet in the feed and get its URL
                tweet_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/status/']")
                if tweet_links:
                    # Get the href attribute of the first tweet link (most recent)
                    tweet_href = tweet_links[0].get_attribute("href")
                    if "status" in tweet_href:
                        return tweet_href
            
            return None
            
        except Exception as e:
            print(f"Error posting tweet: {e}")
            return None
    
    def run_complete_workflow(self, post_content: str, first_name: str = "John", 
                            last_name: str = "Doe", password: str = "SecurePass123!") -> Optional[str]:
        """Run the complete workflow: create email, use proxy, create account, post tweet"""
        print("Starting complete Twitter posting workflow...")
        
        # Get a proxy to use
        proxy = self.proxy_manager.get_next_proxy()
        if not proxy:
            print("No working proxies available")
            return None
        
        print(f"Using proxy: {proxy}")
        
        # Setup driver with proxy
        self.setup_driver(proxy)
        
        try:
            # Create temporary email
            email_result = self.email_handler.create_temp_email()
            if not email_result:
                print("Failed to create temporary email")
                return None
            
            temp_email = email_result['email']
            print(f"Created temporary email: {temp_email}")
            
            # Create Twitter account with temporary email
            success = self.create_twitter_account(first_name, last_name, temp_email, password)
            if not success:
                print("Failed to create Twitter account")
                return None
            
            print("Twitter account created successfully")
            
            # Wait for verification email
            print("Waiting for verification email...")
            verification_email = self.email_handler.wait_for_verification_email(
                ['verify', 'confirm', 'activation'],
                'twitter'
            )
            
            if not verification_email:
                print("Verification email not received within timeout period")
                return None
            
            print("Verification email received")
            
            # Extract verification link
            verification_link = self.email_handler.extract_verification_link(
                verification_email['content']
            )
            
            if not verification_link:
                print("Could not extract verification link from email")
                return None
            
            print(f"Found verification link: {verification_link}")
            
            # Visit verification link in browser
            self.driver.get(verification_link)
            time.sleep(5)
            
            # At this point, we should be verified
            # Now try to post the tweet
            tweet_url = self.post_tweet(post_content)
            
            if tweet_url:
                print(f"Tweet posted successfully! URL: {tweet_url}")
                return tweet_url
            else:
                print("Failed to post tweet")
                return None
                
        except Exception as e:
            print(f"Error in complete workflow: {e}")
            return None
        finally:
            self.close_driver()