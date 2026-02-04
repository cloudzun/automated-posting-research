#!/usr/bin/env python3
"""
Setup and Verification Script
Installs dependencies and verifies system configuration
"""

import subprocess
import sys
import os
import json
from pathlib import Path


def install_dependencies():
    """Install required Python packages"""
    print("Installing Python dependencies...")
    
    try:
        # Try with --break-system-packages for Debian-based systems
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "--break-system-packages", "-r", "requirements.txt"
        ])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False
    
    return True


def verify_chrome_driver():
    """Verify ChromeDriver is available"""
    print("\nChecking ChromeDriver...")
    
    try:
        # Try to run chromedriver to check if it's accessible
        result = subprocess.run(["chromedriver", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✓ ChromeDriver found: {result.stdout.strip()}")
            return True
        else:
            print("✗ ChromeDriver not found or not executable")
            return False
    except FileNotFoundError:
        print("✗ ChromeDriver not found in PATH")
        print("Please download ChromeDriver from https://chromedriver.chromium.org/")
        return False
    except subprocess.TimeoutExpired:
        print("✗ ChromeDriver check timed out")
        return False


def verify_configs():
    """Verify configuration files exist and have basic structure"""
    print("\nVerifying configuration files...")
    
    config_files = [
        "config/proxy_config.json",
        "config/captcha_config.json", 
        "config/email_config.json"
    ]
    
    all_good = True
    
    for config_file in config_files:
        if not os.path.exists(config_file):
            print(f"✗ Missing config file: {config_file}")
            all_good = False
            continue
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Basic validation
            if config_file == "config/captcha_config.json":
                if not config.get('api_key'):
                    print(f"⚠ API key not set in {config_file}")
            elif config_file == "config/proxy_config.json":
                if not config.get('proxy_providers'):
                    print(f"⚠ No proxy providers configured in {config_file}")
            
            print(f"✓ {config_file} exists and is valid JSON")
            
        except json.JSONDecodeError:
            print(f"✗ Invalid JSON in {config_file}")
            all_good = False
        except Exception as e:
            print(f"✗ Error reading {config_file}: {e}")
            all_good = False
    
    return all_good


def verify_python_version():
    """Verify Python version is sufficient"""
    print("\nChecking Python version...")
    
    if sys.version_info >= (3, 7):
        print(f"✓ Python version {sys.version_info.major}.{sys.version_info.minor} is sufficient")
        return True
    else:
        print(f"✗ Python version {sys.version} is too old. Requires 3.7+")
        return False


def verify_directories():
    """Verify required directories exist"""
    print("\nChecking required directories...")
    
    dirs = ["config", "modules", "utils"]
    all_exist = True
    
    for d in dirs:
        if not os.path.isdir(d):
            print(f"✗ Directory missing: {d}")
            all_exist = False
        else:
            print(f"✓ Directory exists: {d}")
    
    return all_exist


def main():
    """Main verification function"""
    print("System Setup and Verification")
    print("=" * 40)
    
    # Check Python version
    python_ok = verify_python_version()
    
    # Check directories
    dirs_ok = verify_directories()
    
    # Install dependencies
    deps_ok = install_dependencies()
    
    # Check ChromeDriver
    chrome_ok = verify_chrome_driver()
    
    # Check configs
    config_ok = verify_configs()
    
    print("\n" + "=" * 40)
    print("VERIFICATION SUMMARY")
    print("=" * 40)
    
    checks = [
        ("Python Version ≥ 3.7", python_ok),
        ("Required Directories", dirs_ok),
        ("Dependencies Installed", deps_ok),
        ("ChromeDriver Available", chrome_ok),
        ("Configuration Files", config_ok)
    ]
    
    all_passed = True
    for name, passed in checks:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:<10} {name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All checks passed! System is ready.")
        print("\nTo run the Twitter bot:")
        print("  python -c \"from modules.workflow_manager import WorkflowManager; manager = WorkflowManager(); manager.run_diagnostic()\"")
    else:
        print("❌ Some checks failed. Please address the issues above.")
        print("\nFor setup instructions, see README.md")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())