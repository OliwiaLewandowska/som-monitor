# SOM Monitor - Complete Project Structure

## Directory Layout

```
som-monitor/
│
├── README.md                      # Main documentation
├── LICENSE                        # MIT License
├── CONTRIBUTING.md                # Contribution guidelines
├── CHANGELOG.md                   # Version history
├── PROJECT_STRUCTURE.md           # This file
│
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup script
├── Makefile                       # Build commands
├── Dockerfile                     # Docker container
├── docker-compose.yml             # Docker compose config
│
├── .env.example                   # Environment template
├── .env                          # Environment variables (not in git)
├── .gitignore                    # Git ignore rules
│
├── __init__.py                   # Package initialization
├── config.py                     # Configuration settings
├── models.py                     # Data models
├── llm_client.py                 # LLM API clients
├── analyzer.py                   # Response analyzer
├── storage.py                    # Data persistence
├── monitor.py                    # Core monitoring logic
├── main.py                       # CLI entry point
├── app.py                        # Streamlit dashboard
├── utils.py                      # Utility functions
├── analysis.py                   # Statistical analysis
├── visualizations.py             # Custom visualizations
│
├── data/                         # Data directory (created automatically)
│   ├── som_results_*.json        # Survey results
│   └── som_history.csv           # Historical data
│
├── logs/                         # Log files (created automatically)
│   └── daily_*.log               # Daily run logs
│
├── tests/                        # Unit tests
│   ├── __init__.py
│   └── test_monitor.py           # Monitor tests
│
├── examples/                     # Example scripts
│   ├── example_usage.ipynb       # Jupyter notebook
│   └── quick_start.py            # Quick start script
│
└── scripts/                      # Utility scripts
    ├── setup.sh                  # Setup script
    └── run_daily.sh              # Daily cron script
```

## File Descriptions

### Core Files

#### `config.py`
- Configuration settings
- API keys
- Brand list
- Query templates
- Model specifications

#### `models.py`
- Data classes: `BrandMention`, `QueryResult`, `SOMMetrics`, `SOMReport`
- Type definitions
- Serialization methods

#### `llm_client.py`
- Abstract `LLMClient` base class
- `OpenAIClient` implementation
- `LLMClientFactory` for creating clients
- Extensible for new providers

#### `analyzer.py`
- `ResponseAnalyzer` class
- Brand mention extraction
- Position tracking
- Mention order calculation

#### `storage.py`
- `StorageManager` class
- JSON file operations
- CSV history management
- Data loading/saving

#### `monitor.py`
- `SOMMonitor` main class
- Survey execution
- Metrics calculation
- Report generation

#### `main.py`
- CLI interface
- Argument parsing
- Survey orchestration
- Console output

#### `app.py`
- Streamlit dashboard
- 4 main tabs: Overview, Rankings, Detailed Analysis, Sample Responses
- Interactive visualizations
- File selection and filtering

#### `utils.py`
- Helper functions
- Data formatting
- File operations
- Common utilities

#### `analysis.py`
- `StatisticalAnalyzer` class
- Confidence intervals
- Significance testing
- Trend detection
- Power analysis

#### `visualizations.py`
- Custom chart functions
- Plotly visualizations
- Radar charts, heatmaps, time series
- Advanced plot types

### Configuration Files

#### `.env`
```bash
OPENAI_API_KEY=your-key-here
# Add more API keys as needed
```

#### `requirements.txt`
```
openai>=1.0.0
pandas>=2.0.0
streamlit>=1.28.0
plotly>=5.17.0
scipy>=1.11.0
python-dotenv>=1.0.0
```

### Scripts

#### `scripts/setup.sh`
- Initial project setup
- Virtual environment creation
- Dependency installation
- Directory creation

#### `scripts/run_daily.sh`
- Automated daily surveys
- Logging
- Error handling
- Cleanup

### Tests

#### `tests/test_monitor.py`
- Unit tests for `ResponseAnalyzer`
- Unit tests for `SOMMonitor`
- Model tests
- Integration tests

### Examples

#### `examples/quick_start.py`
- Simple usage example
- Command-line interface
- Basic survey execution

#### `examples/example_usage.ipynb`
- Jupyter notebook tutorial
- Step-by-step examples
- Visualization examples
- Data analysis workflows

## Data Flow

```
1. Configuration (config.py)
   ↓
2. LLM Client (llm_client.py)
   ↓
3. Query Execution (monitor.py)
   ↓
4. Response Analysis (analyzer.py)
   ↓
5. Data Storage (storage.py)
   ↓
6. Visualization (app.py / visualizations.py)
```

## Component Dependencies

```
main.py
  ├── monitor.py
  │   ├── llm_client.py
  │   ├── analyzer.py
  │   ├── storage.py
  │   └── models.py
  └── config.py

app.py
  ├── monitor.py
  ├── storage.py
  ├── visualizations.py
  └── config.py

analysis.py
  ├── models.py
  └── scipy
```

## Extension Points

### Adding New LLM Providers

1. Create new client class in `llm_client.py`
2. Inherit from `LLMClient`
3. Implement required methods
4. Register with `LLMClientFactory`

### Adding New Metrics

1. Add calculation in `monitor.py`
2. Update `SOMMetrics` model in `models.py`
3. Add visualization in `app.py`
4. Update tests

### Adding New Query Categories

1. Add to `QUERY_TEMPLATES` in `config.py`
2. Test with surveys
3. Update documentation

### Adding New Visualizations

1. Create function in `visualizations.py`
2. Add to dashboard in `app.py`
3. Test with real data
4. Document parameters

## Development Workflow

### Setting Up Development Environment

```bash
# Clone repository
git clone <repo-url>
cd som-monitor

# Run setup script
bash scripts/setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
python -m pytest tests/test_monitor.py -v

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html
```

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Type checking (if using mypy)
mypy *.py
```

### Running the Application

```bash
# CLI - Quick test
python main.py --categories general --runs 2

# CLI - Full survey
make run-full

# Dashboard
make dashboard

# Docker
docker-compose up
```

## Deployment

### Docker Deployment

```bash
# Build image
docker build -t som-monitor .

# Run dashboard
docker run -p 8501:8501 -e OPENAI_API_KEY=your-key som-monitor

# Or use docker-compose
docker-compose up
```

### Production Considerations

1. **API Key Security**: Use environment variables or secret management
2. **Rate Limiting**: Implement backoff strategies
3. **Data Backup**: Regular backups of data directory
4. **Monitoring**: Set up logging and alerting
5. **Scaling**: Consider async processing for large surveys

## Maintenance

### Regular Tasks

- Weekly: Run surveys to collect fresh data
- Monthly: Review and update query templates
- Quarterly: Update dependencies
- As needed: Add new LLM providers

### Updating Dependencies

```bash
# Check for updates
pip list --outdated

# Update specific package
pip install --upgrade openai

# Update all
pip install --upgrade -r requirements.txt

# Freeze new versions
pip freeze > requirements.txt
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all files are in the same directory or Python path is set
2. **API Errors**: Check API key and credits
3. **Data Not Saving**: Verify data/ directory exists and has write permissions
4. **Dashboard Not Loading**: Check if data files exist in data/

### Debug Mode

```python
# Add to main.py or monitor.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Resources

- [OpenAI API Docs](https://platform.openai.com/docs)
- [Streamlit Docs](https://docs.streamlit.io)
- [Plotly Docs](https://plotly.com/python/)
- [Pandas Docs](https://pandas.pydata.org/docs/)

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## License

MIT License - See [LICENSE](LICENSE) file for details.
