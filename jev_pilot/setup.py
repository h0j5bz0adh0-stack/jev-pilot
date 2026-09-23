import sys
import getpass
from .client import JevPilot

def main():
    print("=" * 55)
    print("🚀 jev-pilot Quick Setup & Key Configuration")
    print("=" * 55)
    print("Get your TypeSafe Jev API key at: https://console.typesafe.ai\n")
    
    if len(sys.argv) > 1 and sys.argv[1].startswith("apikey_"):
        key = sys.argv[1].strip()
    else:
        key = input("Enter your TypeSafe Jev API Key: ").strip()

    if not key:
        print("❌ Error: No API key provided.")
        sys.exit(1)

    msg = JevPilot.configure(key)
    print(f"\n✅ {msg}")
    print("🎉 You are ready! Agents and scripts can now use JevPilot without passing keys.")

if __name__ == "__main__":
    main()
