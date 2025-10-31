"""
Quick start example for SOM Monitor
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from monitor import SOMMonitor
from config import BRANDS_TO_TRACK


def main():
    """Run a simple SOM survey"""
    print("🚀 SOM Monitor - Quick Start Example\n")
    
    # Initialize monitor
    print("Initializing monitor...")
    monitor = SOMMonitor(brands=BRANDS_TO_TRACK)
    
    # Run a small survey
    print("\nRunning survey (this will take a few minutes)...")
    print("  Provider: OpenAI")
    print("  Model: gpt-4o")
    print("  Categories: general, code")
    print("  Runs per query: 2\n")
    
    try:
        results = monitor.run_survey(
            provider="openai",
            models=["gpt-4o"],
            categories=["general", "code"],
            runs_per_query=2
        )
        
        print(f"\n✅ Survey complete! Collected {len(results)} responses.\n")
        
        # Generate report
        print("Generating report...\n")
        report = monitor.generate_report(results)
        monitor.print_report(report)
        
        print("\n💡 Next steps:")
        print("  1. View detailed results: streamlit run app.py")
        print("  2. Run more comprehensive survey: python main.py --categories general code enterprise --runs 5")
        print("  3. Check data directory for saved results")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure your OPENAI_API_KEY environment variable is set")
        print("  2. Check your internet connection")
        print("  3. Verify you have API credits available")


if __name__ == "__main__":
    main()
