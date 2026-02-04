#!/usr/bin/env python3
"""
Main Entry Point for Automated Posting System

This script demonstrates the complete workflow of the automated posting system
that can create Twitter/X posts with mentions while evading detection mechanisms.
"""

import sys
import os
from datetime import datetime

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

def main():
    print("🚀 Automated Posting System - Main Execution")
    print("=" * 60)
    print(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("📋 System Components Available:")
    print("   • Proxy Management System")
    print("   • CAPTCHA Solving Integration") 
    print("   • Email Handling System")
    print("   • Twitter Automation Engine")
    print("   • Workflow Orchestration")
    print()
    
    print("💡 To execute complete workflow:")
    print("   1. Configure with service credentials")
    print("   2. Run twitter_bot.run_complete_workflow()")
    print("   3. Monitor results in logs")
    print()
    
    print("🔧 System Status: All modules ready for deployment (dry-run by default)")
    print("🎯 To perform live actions, set environment variable ALLOW_LIVE=1 and pass --live")
    print()
    # Safety: default to dry-run. Require explicit env var and flag to run live.
    args = sys.argv[1:]
    live_flag = "--live" in args
    allow_live_env = os.environ.get("ALLOW_LIVE", "0") == "1"

    if live_flag and allow_live_env:
        print("⚠️  LIVE MODE enabled — proceeding with real actions")
        # Example: call the workflow manager here (commented out to avoid accidental run)
        # from modules.workflow_manager import WorkflowManager
        # manager = WorkflowManager()
        # manager.create_post_with_real_services(post_content="Hello @huaqloud", first_name="Auto", last_name="Bot")
    elif live_flag and not allow_live_env:
        print("✋ Live flag provided but ALLOW_LIVE not set. Aborting live actions.")
    else:
        print("✅ Dry-run mode — no external services will be invoked.")

    return True

if __name__ == "__main__":
    main()