#!/usr/bin/env python3
"""
Example script demonstrating the Twitter bot functionality
"""

from modules.workflow_manager import WorkflowManager


def main():
    print("Twitter Bot Example")
    print("=" * 30)
    
    # Create workflow manager
    manager = WorkflowManager()
    
    # Run diagnostics first
    print("Running diagnostics...")
    manager.run_diagnostic()
    
    print("\n" + "-" * 30)
    print("To actually run the bot, you need to:")
    print("1. Configure your proxy settings in config/proxy_config.json")
    print("2. Add your CAPTCHA service API key to config/captcha_config.json")
    print("3. Ensure ChromeDriver is installed and in PATH")
    print("4. Run the complete workflow (see example below)")
    print()
    print("# Example usage (uncomment to run):")
    print("# result = manager.create_post_with_real_services(")
    print("#     post_content=\"This is an automated tweet!\",")
    print("#     first_name=\"Auto\",")
    print("#     last_name=\"Bot\",")
    print("#     password=\"SecurePassword123!\"")
    print("# )")
    print()


if __name__ == "__main__":
    main()