#!/usr/bin/env python3
"""
Automated Posting System - Main Entry Point

This is the main entry point for the automated posting system.
It demonstrates the complete workflow from account creation to posting.
"""

import sys
import os
from datetime import datetime

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

def main():
    print("🚀 Automated Posting System - Main Interface")
    print("=" * 50)
    print("Available modules:")
    print("  1. Proxy Manager - IP rotation system")
    print("  2. CAPTCHA Solver - Automated verification")
    print("  3. Email Handler - Temporary email management")
    print("  4. Twitter Bot - Main automation engine")
    print("  5. Workflow Manager - End-to-end orchestration")
    print()
    print("For complete workflow execution, use:")
    print("  python3 scripts/run_full_workflow.py")
    print()

if __name__ == "__main__":
    main()