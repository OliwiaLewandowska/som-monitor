"""
CLI entry point for SOM Monitor
"""
import argparse
from dotenv import load_dotenv
from pathlib import Path
from monitor import SOMMonitor
from config import BRANDS_TO_TRACK, MODELS

# Load environment variables from .env file
load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Share of Model Monitor")
    
    parser.add_argument(
        '--provider',
        default='openai',
        help='LLM provider (default: openai)'
    )
    
    parser.add_argument(
        '--models',
        nargs='+',
        default=['gpt-4o'],
        help='Models to query (default: gpt-4o)'
    )
    
    parser.add_argument(
        '--categories',
        nargs='+',
        default=None,  # Will use enabled categories from config
        help='Query categories (if not specified, uses enabled categories from config)'
    )
    
    parser.add_argument(
        '--runs',
        type=int,
        default=3,
        help='Runs per query (default: 3)'
    )
    
    parser.add_argument(
        '--brands',
        nargs='+',
        default=None,
        help=f'Brands to track (default: {", ".join(BRANDS_TO_TRACK)})'
    )
    
    parser.add_argument(
        '--report-only',
        action='store_true',
        help='Only generate report from existing data'
    )
    
    parser.add_argument(
        '--merge-previous',
        action='store_true',
        help='Merge new results with most recent existing results'
    )
    
    args = parser.parse_args()
    
    # Initialize monitor
    monitor = SOMMonitor(brands=args.brands)
    
    if args.report_only:
        # Load existing results and generate report
        results = monitor.load_results()
        if results:
            report = monitor.generate_report(results)
            monitor.print_report(report)
        else:
            print("No existing results found.")
    else:
        # Run survey
        print(f"\n🚀 Starting SOM Survey")
        print(f"Provider: {args.provider}")
        print(f"Models: {', '.join(args.models)}")
        print(f"Categories: {'Using enabled categories from config' if args.categories is None else ', '.join(args.categories)}")
        print(f"Runs per query: {args.runs}")
        print(f"Brands: {', '.join(args.brands or BRANDS_TO_TRACK)}\n")
        
        # Get previous results if merging
        previous_results = []
        if args.merge_previous:
            previous_results = monitor.storage.load_results()
            if previous_results:
                print(f"\n📥 Loaded {len(previous_results)} previous results to merge")
            
        # Run new survey
        new_results = monitor.run_survey(
            provider=args.provider,
            models=args.models,
            categories=args.categories,
            runs_per_query=args.runs
        )
        
        # Merge results if needed
        if args.merge_previous and previous_results:
            results = previous_results + new_results
            # Save merged results
            monitor.storage.save_results(results)
        else:
            results = new_results
        
        # Generate and print report
        if results:
            report = monitor.generate_report(results)
            monitor.print_report(report)
            
            print("\n💡 Tip: Run 'streamlit run app.py' to visualize results")


if __name__ == "__main__":
    main()
