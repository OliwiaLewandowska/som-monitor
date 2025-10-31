# SOM Monitor - Quick Reference Guide

## Installation

```bash
# Basic setup
git clone <repo-url> && cd som-monitor
pip install -r requirements.txt
export OPENAI_API_KEY='your-key'

# Or use setup script
bash scripts/setup.sh
```

## Common Commands

### Run Surveys

```bash
# Basic survey (default: general category, 3 runs)
python main.py

# Specific categories
python main.py --categories general code enterprise

# More runs for better statistics
python main.py --categories general --runs 10

# Multiple models
python main.py --models gpt-4o gpt-4o-mini

# Full survey
python main.py --categories general code enterprise reasoning cost --runs 5
```

### Dashboard

```bash
# Launch dashboard
streamlit run app.py

# Or use Makefile
make dashboard

# Access at http://localhost:8501
```

### Using Make

```bash
make install     # Install dependencies
make setup       # Initial setup
make run         # Run basic survey
make run-full    # Run comprehensive survey
make dashboard   # Launch dashboard
make test        # Run tests
make clean       # Clean up files
```

## Configuration Quick Edit

### Edit Brands (config.py)

```python
BRANDS_TO_TRACK = [
    "OpenAI",
    "Anthropic", 
    "Google",
    "YourBrand"  # Add your brand
]
```

### Add Query Category (config.py)

```python
QUERY_TEMPLATES = {
    "your_category": [
        "Your question 1?",
        "Your question 2?",
    ]
}
```

### Change Survey Settings (config.py)

```python
RUNS_PER_QUERY = 5       # More runs = better stats
TEMPERATURE = 0.7        # 0 = deterministic, 1 = creative
MAX_TOKENS = 1000        # Response length
RATE_LIMIT_DELAY = 1     # Seconds between requests
```

## Python API

### Basic Usage

```python
from monitor import SOMMonitor

# Initialize
monitor = SOMMonitor(brands=["OpenAI", "Anthropic"])

# Run survey
results = monitor.run_survey(
    provider="openai",
    models=["gpt-4o"],
    categories=["general"],
    runs_per_query=3
)

# Get metrics
metrics = monitor.calculate_som()

# Print report
report = monitor.generate_report()
monitor.print_report(report)
```

### Advanced Usage

```python
from monitor import SOMMonitor
from storage import StorageManager
from analysis import StatisticalAnalyzer

# Initialize
monitor = SOMMonitor()
storage = StorageManager()
analyzer = StatisticalAnalyzer()

# Load historical data
history = storage.get_history_df()

# Compare two brands
comparison = analyzer.compare_brands(
    results, 
    "OpenAI", 
    "Anthropic"
)

# Detect trends
trend = analyzer.detect_trend([0.5, 0.6, 0.65, 0.7])
```

## Data Access

### Load Results

```python
from storage import StorageManager

storage = StorageManager()

# Load latest results
results = storage.load_results()

# Load specific file
results = storage.load_results("som_results_20240101_120000.json")

# Get all result files
files = storage.get_results_files()

# Load history as DataFrame
df = storage.get_history_df()
```

### Query Results

```python
# Filter by category
general_results = [r for r in results if r.category == "general"]

# Filter by brand mention
openai_mentions = [r for r in results if r.mentions["OpenAI"].mentioned]

# Get first mentions only
first_mentions = [r for r in results if r.mention_order and r.mention_order[0] == "OpenAI"]
```

## Visualization Examples

### Custom Charts

```python
from visualizations import *
import plotly.graph_objects as go

# Comparison chart
fig = create_comparison_chart(metrics, "mention_rate")
fig.show()

# Radar chart
fig = create_radar_chart(metrics)
fig.show()

# Time series
fig = create_time_series_chart(history_df, brands)
fig.show()

# Heatmap
fig = create_heatmap(results, brands)
fig.show()
```

## Statistical Analysis

### Confidence Intervals

```python
from analysis import StatisticalAnalyzer

analyzer = StatisticalAnalyzer(confidence_level=0.95)

# Get mention rates for a brand
mentions = [1 if r.mentions["OpenAI"].mentioned else 0 for r in results]

# Calculate CI
mean, lower, upper = analyzer.calculate_confidence_interval(mentions)
print(f"Mention rate: {mean:.1%} ({lower:.1%} - {upper:.1%})")
```

### Compare Brands

```python
# Statistical comparison
comparison = analyzer.compare_brands(results, "OpenAI", "Anthropic")

print(f"OpenAI: {comparison['rate1']:.1%}")
print(f"Anthropic: {comparison['rate2']:.1%}")
print(f"Difference: {comparison['difference']:.1%}")
print(f"Significant: {comparison['significant']}")
print(f"Effect size: {comparison['effect_size']:.2f}")
```

### Trend Detection

```python
# Historical mention rates
rates = [0.45, 0.50, 0.52, 0.55, 0.58]

trend_info = analyzer.detect_trend(rates)
print(f"Trend: {trend_info['trend']}")
print(f"Significant: {trend_info['significant']}")
```

## Docker Commands

```bash
# Build image
docker build -t som-monitor .

# Run dashboard
docker run -p 8501:8501 -e OPENAI_API_KEY=$OPENAI_API_KEY som-monitor

# Run survey
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY som-monitor python main.py

# Using docker-compose
docker-compose up                    # Start dashboard
docker-compose run som-cli           # Run survey
docker-compose down                  # Stop all
```

## Scheduled Surveys

### Using Cron

```bash
# Edit crontab
crontab -e

# Add daily run at 9 AM
0 9 * * * /path/to/som-monitor/scripts/run_daily.sh

# Add weekly run on Monday at 8 AM
0 8 * * 1 cd /path/to/som-monitor && python main.py --categories general code --runs 5
```

### Manual Schedule

```bash
# Create a simple scheduler script
while true; do
    python main.py --categories general --runs 3
    sleep 86400  # 24 hours
done
```

## Exporting Data

### To CSV

```python
import pandas as pd

# Export metrics
df = pd.DataFrame([m.to_dict() for m in metrics.values()])
df.to_csv('metrics.csv', index=False)

# Export results
rows = []
for r in results:
    for brand, mention in r.mentions.items():
        rows.append({
            'timestamp': r.timestamp,
            'brand': brand,
            'mentioned': mention.mentioned,
            'category': r.category
        })
df = pd.DataFrame(rows)
df.to_csv('results.csv', index=False)
```

### To JSON

```python
import json

# Export report
with open('report.json', 'w') as f:
    json.dump(report.to_dict(), f, indent=2)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API key error | `export OPENAI_API_KEY='your-key'` |
| Import errors | Ensure files in same directory or use `sys.path.append()` |
| No results | Check `data/` directory exists |
| Dashboard empty | Run survey first with `python main.py` |
| Rate limits | Increase `RATE_LIMIT_DELAY` in config.py |
| Out of memory | Reduce `RUNS_PER_QUERY` or process in batches |

## Performance Tips

- **Faster surveys**: Use fewer runs (`--runs 2`)
- **Better statistics**: Use more runs (`--runs 10+`)
- **Multiple models**: Run sequentially to avoid rate limits
- **Large datasets**: Process in batches using `utils.batch_items()`
- **Long responses**: Reduce `MAX_TOKENS` in config.py

## Best Practices

1. **Start small**: Begin with 2-3 runs to test
2. **Validate queries**: Ensure questions are neutral
3. **Regular runs**: Weekly surveys for trend tracking
4. **Backup data**: Copy `data/` directory regularly
5. **Version control**: Commit config changes
6. **Document changes**: Update CHANGELOG.md

## Getting Help

```bash
# CLI help
python main.py --help

# Check logs
tail -f logs/daily_*.log

# Run tests
python -m pytest tests/ -v

# Check version
python -c "import __init__; print(__init__.__version__)"
```

## Quick Debugging

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test single query
from llm_client import OpenAIClient
client = OpenAIClient()
response = client.query("What are the best LLMs?", model="gpt-4o")
print(response)

# Test analyzer
from analyzer import ResponseAnalyzer
analyzer = ResponseAnalyzer(["OpenAI", "Anthropic"])
mentions, order, total = analyzer.analyze(response)
print(f"Mentions: {mentions}")
print(f"Order: {order}")
```

## Resources

- 📚 Full docs: [README.md](README.md)
- 🏗️ Architecture: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- 🤝 Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- 📝 Changes: [CHANGELOG.md](CHANGELOG.md)