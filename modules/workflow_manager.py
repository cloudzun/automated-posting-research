"""
Workflow Manager
Coordinates the end-to-end process of creating posts with temporary emails, proxies, and CAPTCHA solving
"""

import json
import time
from typing import Optional, Dict, Any
from modules.twitter_bot import TwitterBot


class WorkflowManager:
    def __init__(self):
        self.bot = TwitterBot()
    
    def create_post_with_real_services(self, 
                                     post_content: str,
                                     first_name: str = "John", 
                                     last_name: str = "Doe", 
                                     password: str = "SecurePass123!",
                                     max_retries: int = 3) -> Optional[Dict[str, Any]]:
        """
        Create a post using real temporary email, proxy, and CAPTCHA solving services
        
        Args:
            post_content: Content to post
            first_name: First name for account creation
            last_name: Last name for account creation
            password: Password for account
            max_retries: Maximum number of retry attempts
        
        Returns:
            Dictionary with success status and tweet URL if successful
        """
        print("=" * 60)
        print("STARTING TWITTER POST CREATION WORKFLOW")
        print("=" * 60)
        
        for attempt in range(max_retries):
            print(f"\nAttempt {attempt + 1} of {max_retries}")
            print("-" * 30)
            
            try:
                result = self.bot.run_complete_workflow(
                    post_content=post_content,
                    first_name=first_name,
                    last_name=last_name,
                    password=password
                )
                
                if result:
                    print("\n" + "=" * 60)
                    print("SUCCESS! Tweet created successfully.")
                    print(f"Tweet URL: {result}")
                    print("=" * 60)
                    
                    return {
                        "success": True,
                        "tweet_url": result,
                        "attempt": attempt + 1,
                        "error": None
                    }
                else:
                    print(f"Attempt {attempt + 1} failed")
                    if attempt < max_retries - 1:
                        print("Retrying...")
                        time.sleep(10)  # Wait before retry
            
            except Exception as e:
                print(f"Error during attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    time.sleep(10)
        
        print("\n" + "=" * 60)
        print("FAILED to create tweet after all attempts")
        print("=" * 60)
        
        return {
            "success": False,
            "tweet_url": None,
            "attempt": max_retries,
            "error": "All attempts failed"
        }
    
    def validate_configurations(self) -> Dict[str, bool]:
        """
        Validate that all required configurations are properly set up
        """
        validations = {}
        
        # Check if required config files exist
        import os
        config_files = [
            "config/proxy_config.json",
            "config/captcha_config.json", 
            "config/email_config.json"
        ]
        
        for config_file in config_files:
            validations[config_file] = os.path.exists(config_file)
        
        # Check if API keys are filled in (basic check)
        try:
            with open("config/captcha_config.json", 'r') as f:
                captcha_config = json.load(f)
                validations["captcha_api_key"] = bool(captcha_config.get("api_key"))
        except:
            validations["captcha_api_key"] = False
        
        try:
            with open("config/proxy_config.json", 'r') as f:
                proxy_config = json.load(f)
                # Check if there are any proxies configured
                proxies_available = False
                for provider in proxy_config["proxy_providers"]:
                    if provider["provider"] == "custom" and provider.get("proxies"):
                        proxies_available = True
                        break
                    elif provider["provider"] != "custom" and provider.get("username"):
                        proxies_available = True
                        break
                validations["proxies_configured"] = proxies_available
        except:
            validations["proxies_configured"] = False
        
        return validations
    
    def run_diagnostic(self):
        """
        Run a diagnostic check of the system
        """
        print("Running system diagnostic...")
        print("-" * 30)
        
        validations = self.validate_configurations()
        
        print("Configuration Validation:")
        for item, valid in validations.items():
            status = "✓" if valid else "✗"
            print(f"  {status} {item}: {'Valid' if valid else 'Invalid/Not Found'}")
        
        print("\nRequired Actions:")
        issues = [item for item, valid in validations.items() if not valid]
        if not issues:
            print("  ✓ All configurations are valid!")
        else:
            for issue in issues:
                if "proxy" in issue.lower():
                    print("  - Configure proxy settings in config/proxy_config.json")
                elif "captcha" in issue.lower():
                    print("  - Add CAPTCHA API key to config/captcha_config.json")
                elif "email" in issue.lower():
                    print("  - Verify email configuration in config/email_config.json")
                else:
                    print(f"  - Fix: {issue}")
        
        print("-" * 30)


def main():
    """
    Example usage of the WorkflowManager
    """
    manager = WorkflowManager()
    
    # Run diagnostics first
    manager.run_diagnostic()
    
    # Example: Create a post
    # NOTE: This is commented out as it requires valid API keys and services
    # Uncomment and configure properly to test
    
    # result = manager.create_post_with_real_services(
    #     post_content="This is an automated tweet created through our system!",
    #     first_name="Auto",
    #     last_name="Bot",
    #     password="ComplexPassword123!"
    # )
    # 
    # if result["success"]:
    #     print(f"Tweet created successfully: {result['tweet_url']}")
    # else:
    #     print(f"Failed to create tweet: {result['error']}")


if __name__ == "__main__":
    main()