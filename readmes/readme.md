# SOM Monitor - Share of Model Tracking System

Track how different LLMs mention various AI brands to understand market perception and positioning.

## Features

- 📊 **Multi-LLM Support**: Currently supports OpenAI (easily extensible)
- 📈 **Comprehensive Metrics**: Mention rate, first mention rate, position tracking
- 🎯 **Category Analysis**: Track performance across different query types
- 📉 **Historical Tracking**: Store and analyze trends over time
- 🎨 **Interactive Dashboard**: Beautiful Streamlit visualization
- 💾 **Persistent Storage**: JSON and CSV storage for analysis

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd som-monitor

# Install dependencies
pip install -r requirements.txt

# Set up your API key
export OPENAI_API_KEY='your-openai-api-key'
```

## Project Structure

```
som-monitor/
├── config.py          # Configuration and settings
├── models.py          # Data models
├── llm_client.py      # LLM API clients
├── analyzer.py        # Response analysis
├── storage.py         # Data persistence
├── monitor.py         # Core monitoring logic
├── main.py            # CLI entry point
├── app.py             # Streamlit dashboard
├── requirements.txt   # Python dependencies
├── README.md          # This file
└── data/              # Storage directory (created automatically)
    ├── som_results_*.json
    └── som_history.csv
```

## Quick Start

### 1. Run a Survey

```bash
# Basic survey with default settings
python main.py

# Custom survey with specific parameters
python main.py --categories general code enterprise --runs 5 --models gpt-4o gpt-4o-mini

# Available options:
# --provider: LLM provider (default: openai)
# --models: Models to query (default: gpt-4o)
# --categories: Query categories (general, code, enterprise, reasoning, cost)
# --runs: Number of runs per query (default: 3)
# --brands: Brands to track (default: OpenAI, Anthropic, Google, Meta, Cohere, Mistral, xAI)
```

### 2. View Results in Dashboard

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`

### 3. Generate Report from Existing Data

```bash
python main.py --report-only
```

## Dashboard Features

### 📈 Overview Tab
- Key metrics and top brands
- Mention rate visualization
- First mention rate charts

### 🏆 Rankings Tab
- Comprehensive brand comparison table
- Average position analysis
- Performance rankings

### 📊 Detailed Analysis Tab
- Performance breakdown by category
- Mention count distribution
- Brand co-occurrence matrix

### 💬 Sample Responses Tab
- Browse actual LLM responses
- Filter by brand and category
- Inspect mention patterns

## Configuration

Edit `config.py` to customize:

```python
# Brands to track
BRANDS_TO_TRACK = [
    "OpenAI", "Anthropic", "Google", 
    "Meta", "Cohere", "Mistral", "xAI"
]

# Query templates
QUERY_TEMPLATES = {
    "general": [...],
    "code": [...],
    # Add your own categories
}

# Sampling parameters
RUNS_PER_QUERY = 3
TEMPERATURE = 0.7
```

## Adding New LLM Providers

1. Create a new client class in `llm_client.py`:

```python
class AnthropicClient(LLMClient):
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self._provider_name = "anthropic"
    
    @property
    def provider_name(self) -> str:
        return self._provider_name
    
    def query(self, prompt: str, model: str, temperature: float, max_tokens: int):
        # Implementation
        pass
```

2. Register the client:

```python
LLMClientFactory.register("anthropic", AnthropicClient)
```

3. Update `config.py`:

```python
MODELS = {
    "openai": ["gpt-4o", "gpt-4o-mini"],
    "anthropic": ["claude-sonnet-4-5"]
}
```

## Metrics Explained

- **Mention Rate**: Percentage of queries where the brand was mentioned
- **First Mention Rate**: Percentage of queries where the brand was mentioned first
- **Average Position**: Average position when mentioned (1 = first, 2 = second, etc.)
- **Total Mentions**: Raw count of mentions across all queries

## Data Storage

- **JSON Files**: Complete query results with metadata (`data/som_results_*.json`)
- **CSV History**: Flattened time-series data for analysis (`data/som_history.csv`)

## Example Use Cases

### Track Your Brand Over Time
```bash
# Run weekly surveys
python main.py --categories general code enterprise --runs 5

# Compare results week-over-week in the dashboard
streamlit run app.py
```

### Competitive Intelligence
```bash
# Deep dive into specific categories
python main.py --categories general --runs 10

# Analyze co-occurrence patterns
# Check which brands are mentioned together
```

### Model Comparison
```bash
# Compare different models' perspectives
python main.py --models gpt-4o gpt-4o-mini --runs 5

# See if cheaper models have different brand bias
```

## Statistical Considerations

- **Sample Size**: Default 3 runs per query (adjust with `--runs`)
- **Temperature**: Set to 0.7 for variety (configurable in `config.py`)
- **Query Diversity**: Multiple categories to capture different contexts
- **Temporal Tracking**: Historical CSV for trend analysis

## Tips for Accurate Results

1. **Run Multiple Times**: Use `--runs 5` or higher for statistical significance
2. **Diverse Queries**: Test multiple categories to avoid bias
3. **Regular Monitoring**: Run weekly to track trends
4. **Query Design**: Craft neutral queries that don't bias responses
5. **Sample Size**: Aim for 50+ total queries for reliable metrics

## Troubleshooting

### API Rate Limits
- Adjust `RATE_LIMIT_DELAY` in `config.py`
- Use fewer concurrent queries

### No Results Found
- Check that `data/` directory exists
- Verify API key is set correctly
- Run a survey first before viewing dashboard

### Missing Brands
- Add to `BRANDS_TO_TRACK` in `config.py`
- Re-run survey to collect new data

## Contributing

To add features:
1. Add new query categories in `config.py`
2. Extend `ResponseAnalyzer` for advanced analysis
3. Add new visualizations to `app.py`
4. Implement additional LLM providers in `llm_client.py`

## License

MIT License

## Future Enhancements

- [ ] Sentiment analysis on mentions
- [ ] Context classification (pricing, features, etc.)
- [ ] Automated scheduling and alerts
- [ ] Statistical significance testing
- [ ] Export reports to PDF
- [ ] Multi-provider comparison
- [ ] A/B testing of query variations