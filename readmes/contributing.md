# Contributing to SOM Monitor

Thank you for your interest in contributing to SOM Monitor! This document provides guidelines for contributions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/som-monitor.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests: `make test`
6. Commit your changes: `git commit -am 'Add some feature'`
7. Push to the branch: `git push origin feature/your-feature-name`
8. Submit a pull request

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest black pylint isort

# Run tests
python -m pytest tests/

# Format code
black *.py
isort *.py

# Lint code
pylint *.py
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Write docstrings for all functions and classes
- Keep functions focused and small
- Add comments for complex logic

## Testing

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage
- Include both positive and negative test cases

## Adding New LLM Providers

To add a new LLM provider:

1. Create a new client class in `llm_client.py`:

```python
class NewProviderClient(LLMClient):
    def __init__(self, api_key: str):
        # Initialize client
        pass
    
    @property
    def provider_name(self) -> str:
        return "newprovider"
    
    def query(self, prompt: str, model: str, temperature: float, max_tokens: int):
        # Implement query logic
        pass
```

2. Register the client:

```python
LLMClientFactory.register("newprovider", NewProviderClient)
```

3. Update `config.py` with new models
4. Add tests in `tests/test_monitor.py`
5. Update documentation

## Adding New Features

### New Metrics

1. Add calculation logic to `monitor.py`
2. Update `models.py` with new data structures
3. Add visualization to `app.py`
4. Write tests
5. Update documentation

### New Query Categories

1. Add templates to `QUERY_TEMPLATES` in `config.py`
2. Test with multiple runs
3. Verify results make sense
4. Document the category

### New Visualizations

1. Add to appropriate tab in `app.py`
2. Use Plotly for consistency
3. Ensure responsive design
4. Add interactivity where useful

## Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Include usage examples
- Update CHANGELOG.md

## Pull Request Process

1. Update README.md with details of changes if needed
2. Update the CHANGELOG.md with your changes
3. Ensure all tests pass
4. Request review from maintainers
5. Address review comments
6. Squash commits before merge if requested

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Questions?

Open an issue or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
