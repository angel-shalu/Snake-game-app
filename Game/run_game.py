#!/usr/bin/env python3
"""
Snake Game Launcher
Choose between basic and enhanced versions of the Snake game.
"""

import subprocess
import sys
import os

def main():
    print("🐍 Snake Game Launcher")
    print("=" * 30)
    print("Choose your game version:")
    print("1. Basic Snake Game (snake_game.py)")
    print("2. Enhanced Snake Game (snake_game_enhanced.py)")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                print("\n🚀 Starting Basic Snake Game...")
                subprocess.run([sys.executable, "-m", "streamlit", "run", "snake_game.py"])
                break
            elif choice == "2":
                print("\n🚀 Starting Enhanced Snake Game...")
                subprocess.run([sys.executable, "-m", "streamlit", "run", "snake_game_enhanced.py"])
                break
            elif choice == "3":
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break

if __name__ == "__main__":
    main() 