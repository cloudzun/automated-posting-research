#!/usr/bin/env python3
"""
Advanced X Account Registration with Selenium
This script uses Selenium WebDriver to perform browser automation
with stealth techniques to avoid detection
"""

import time
import random
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc

def random_delay(min_sec=1, max_sec=3):
    """Introduce random delays to mimic human behavior"""
    time.sleep(random.uniform(min_sec, max_sec))

def get_temp_email():
    """Get the temporary email address from tmpmail"""
    try:
        result = subprocess.run(['/tmp/tmpmail/tmpmail', '--generate'], capture_output=True, text=True, check=True)
        email = result.stdout.strip()
        print(f"Generated temporary email: {email}")
        return email
    except subprocess.CalledProcessError as e:
        print(f"Error getting temporary email: {e}")
        return None

def setup_stealth_driver():
    """Setup Chrome driver with stealth options to avoid detection"""
    options = uc.ChromeOptions()
    
    # Add various options to avoid detection
    options.add_argument("--no-first-run")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-images")
    options.add_argument("--disable-javascript")  # We'll enable selectively
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-ipc-flooding-protection")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-backgrounding-occluded-windows")
    
    # Set a realistic window size
    options.add_argument("--window-size=1366,768")
    
    # Use a realistic user agent
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Initialize the undetected chrome driver
    driver = uc.Chrome(options=options)
    
    # Execute script to remove webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def register_on_x(driver, temp_email):
    """Register an account on X using the temporary email"""
    
    print("Navigating to X registration page...")
    
    try:
        # Navigate to X signup page
        driver.get("https://x.com/i/flow/signup")
        random_delay(3, 5)
        
        print("Page loaded, checking for elements...")
        
        # Wait for the page to load completely
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "input"))
        )
        
        print("Looking for email input field...")
        
        # Find and fill in the email field
        try:
            # Different selectors for X signup page
            email_input_selectors = [
                "input[autocomplete='email']",
                "input[type='email']",
                "input[name='email']",
                "#email",
                ".r-30o5oe",  # X's class for inputs
            ]
            
            email_field = None
            for selector in email_input_selectors:
                try:
                    email_field = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if email_field:
                print(f"Found email field, entering: {temp_email}")
                email_field.clear()
                email_field.send_keys(temp_email)
                
                # Click next button
                next_buttons = [
                    "button[data-testid='next-button']",
                    "button[type='submit']",
                    "button:contains('Next')",
                    ".r-30o5oe.r-1niwhzg.r-17gur6a.r-1yadl64.r-1loqt21.r-xyw6el.r-184en5c"
                ]
                
                next_button = None
                for selector in next_buttons:
                    try:
                        next_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        break
                    except:
                        continue
                
                if next_button:
                    print("Clicking next button...")
                    next_button.click()
                    random_delay(2, 4)
                    
                    # At this point, X might ask for phone number or email verification
                    # If it asks for phone number, we need to indicate we want to use email instead
                    
                    # Check if we're on phone number screen
                    try:
                        phone_screen = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Phone')]"))
                        )
                        
                        if phone_screen:
                            print("Detected phone number screen, looking for email alternative...")
                            
                            # Look for "Use email instead" or similar
                            email_alternative_selectors = [
                                "button:contains('Use email')",
                                "button:contains('Email')",
                                "a:contains('Email')",
                                ".r-30o5oe:contains('Email')"
                            ]
                            
                            email_alt_button = None
                            for selector in email_alternative_selectors:
                                try:
                                    email_alt_button = WebDriverWait(driver, 5).until(
                                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                                    )
                                    break
                                except:
                                    continue
                            
                            if email_alt_button:
                                email_alt_button.click()
                                random_delay(2, 4)
                                
                    except:
                        # If we don't find phone screen, we might be on verification screen
                        print("Continuing with email verification...")
                    
                    print("Registration flow initiated successfully")
                    return True
                else:
                    print("Could not find next button")
                    return False
            else:
                print("Could not find email input field")
                return False
                
        except Exception as e:
            print(f"Error filling email field: {e}")
            return False
            
    except Exception as e:
        print(f"Error during registration: {e}")
        return False

def main():
    print("Starting advanced X registration automation...")
    
    # Get temporary email
    temp_email = get_temp_email()
    
    if not temp_email:
        print("Failed to get temporary email")
        return False
    
    print(f"Using temporary email: {temp_email}")
    
    # Setup stealth driver
    try:
        print("Setting up stealth browser...")
        driver = setup_stealth_driver()
        
        # Register on X
        success = register_on_x(driver, temp_email)
        
        if success:
            print("\nX registration process initiated successfully!")
            print("Note: The process may require additional steps like email verification.")
            print("The browser remains open for manual completion if needed.")
            
            # Keep browser open for a while to allow for email verification
            print("Waiting for potential email verification (5 minutes)...")
            time.sleep(300)  # Wait 5 minutes
            
        else:
            print("\nFailed to initiate X registration.")
        
        # Close the driver
        driver.quit()
        
        return success
        
    except Exception as e:
        print(f"Error setting up or running automation: {e}")
        return False

if __name__ == "__main__":
    main()