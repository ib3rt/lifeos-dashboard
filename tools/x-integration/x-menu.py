#!/usr/bin/env python3
"""X Automation Menu for Life OS"""

import subprocess
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    clear_screen()
    print("╔═══════════════════════════════════════════════════════╗")
    print("║        🐦 X (TWITTER) AUTOMATION MENU           ║")
    print("╚═══════════════════════════════════════════════════════╝")
    print()
    print("  Status: ⚠️  Authentication issue (see README)")
    print()
    print("  1. 📝 Post a tweet")
    print("  2. 📊 Post metrics update")
    print("  3. 🔍 Test API connection")
    print("  4. 📖 View README")
    print("  5. 🔧 Fix authentication")
    print("  6. 🚪 Exit")
    print()
    print("-" * 60)

def main():
    while True:
        show_menu()
        choice = input("  Choose (1-6): ").strip()
        
        if choice == '1':
            tweet = input("\n  Enter your tweet: ").strip()
            if tweet:
                print("\n  🐦 Posting...")
                subprocess.run(['./post-tweet.py', tweet])
                input("\n  Press Enter to continue...")
        
        elif choice == '2':
            from datetime import datetime
            date = datetime.now().strftime("%Y-%m-%d %H:%M")
            tweet = f"📊 Life OS Daily Update - {date} | All systems nominal! 🦾"
            print(f"\n  📊 Posting: {tweet}")
            subprocess.run(['./post-tweet.py', tweet])
            input("\n  Press Enter to continue...")
        
        elif choice == '3':
            print("\n  🔍 Testing API connection...")
            subprocess.run(['./post-tweet.py', 'Test tweet'])
            input("\n  Press Enter to continue...")
        
        elif choice == '4':
            subprocess.run(['cat', 'README.md'])
            input("\n  Press Enter to continue...")
        
        elif choice == '5':
            print("\n  🔧 Check README.md for fix instructions")
            print("  or visit: https://developer.x.com")
            input("\n  Press Enter to continue...")
        
        elif choice == '6':
            print("\n  👋 Goodbye!")
            break
        
        else:
            print("\n  ❌ Invalid choice")
            input("  Press Enter to continue...")

if __name__ == '__main__':
    main()
