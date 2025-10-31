# SOM Monitor - All Files Reference

All files have been created as artifacts in this conversation. Here's the complete list with descriptions:

## Core Application Files

### 1. config.py
**Artifact ID:** `som_config`
- Configuration settings
- API keys
- Brand list
- Query templates

### 2. models.py
**Artifact ID:** `som_models`
- BrandMention dataclass
- QueryResult dataclass
- SOMMetrics dataclass
- SOMReport dataclass

### 3. llm_client.py
**Artifact ID:** `som_llm_client`
- LLMClient base class
- OpenAIClient implementation
- LLMClientFactory

### 4. analyzer.py
**Artifact ID:** `som_analyzer`
- ResponseAnalyzer class
- Brand mention extraction
- Position tracking

### 5. storage.py
**Artifact ID:** `som_storage`
- StorageManager class
- JSON/CSV operations
- History management

### 6. monitor.py
**Artifact ID:** `som_monitor`
- SOMMonitor main class
- Survey execution
- Metrics calculation

### 7. main.py
**Artifact ID:** `som_main`
- CLI interface
- Argument parsing
- Main entry point

### 8. app.py
**Artifact ID:** `som_streamlit`
- Streamlit dashboard
- 4 tabs with visualizations
- Interactive UI

### 9. utils.py
**Artifact ID:** `som_utils`
- Utility functions
- Helper methods
- Data formatting

### 10. analysis.py
**Artifact ID:** `som_analysis`
- StatisticalAnalyzer class
- Confidence intervals
- Significance testing

### 11. visualizations.py
**Artifact ID:** `som_visualizations`
- Custom chart functions
- Plotly visualizations
- Advanced plots

### 12. __init__.py
**Artifact ID:** `som_init`
- Package initialization
- Exports

## Configuration Files

### 13. requirements.txt
**Artifact ID:** `som_requirements`

### 14. setup.py
**Artifact ID:** `som_setup`

### 15. .env.example
**Artifact ID:** `som_env_example`

### 16. .gitignore
**Artifact ID:** `som_gitignore`

### 17. Makefile
**Artifact ID:** `som_makefile`

### 18. Dockerfile
**Artifact ID:** `som_docker`

### 19. docker-compose.yml
**Artifact ID:** `som_docker_compose`

## Documentation

### 20. README.md
**Artifact ID:** `som_readme`

### 21. CONTRIBUTING.md
**Artifact ID:** `som_contributing`

### 22. CHANGELOG.md
**Artifact ID:** `som_changelog`

### 23. LICENSE
**Artifact ID:** `som_license`

### 24. PROJECT_STRUCTURE.md
**Artifact ID:** `som_project_structure`

### 25. QUICKREF.md
**Artifact ID:** `som_quickref`

## Scripts

### 26. scripts/setup.sh
**Artifact ID:** `som_scripts_setup`

### 27. scripts/run_daily.sh
**Artifact ID:** `som_scripts_run`

## Tests

### 28. tests/__init__.py
**Artifact ID:** `som_test_init`

### 29. tests/test_monitor.py
**Artifact ID:** `som_test_monitor`

## Examples

### 30. examples/quick_start.py
**Artifact ID:** `som_example_script`

### 31. examples/example_usage.ipynb
**Artifact ID:** `som_example_notebook`

---

## How to Access

All these files are in the artifacts panel on the right side of this conversation. You can:
1. Click on each artifact to view it
2. Copy the content from each artifact
3. Create the corresponding file in your project

## Quick Setup Script

Save this as `download_all.sh` and run it to see the structure:

```bash
#!/bin/bash
mkdir -p som-monitor/{data,logs,tests,examples,scripts}
cd som-monitor
echo "Create the following files by copying from artifacts:"
echo "  - config.py"
echo "  - models.py"
echo "  - llm_client.py"
echo "  - analyzer.py"
echo "  - storage.py"
echo "  - monitor.py"
echo "  - main.py"
echo "  - app.py"
echo "  - utils.py"
echo "  - analysis.py"
echo "  - visualizations.py"
echo "  - __init__.py"
echo "  - requirements.txt"
echo "  - setup.py"
echo "  - .env.example"
echo "  - .gitignore"
echo "  - Makefile"
echo "  - Dockerfile"
echo "  - docker-compose.yml"
echo "  - README.md"
echo "  - CONTRIBUTING.md"
echo "  - CHANGELOG.md"
echo "  - LICENSE"
echo "  - PROJECT_STRUCTURE.md"
echo "  - QUICKREF.md"
echo "  - scripts/setup.sh"
echo "  - scripts/run_daily.sh"
echo "  - tests/__init__.py"
echo "  - tests/test_monitor.py"
echo "  - examples/quick_start.py"
echo "  - examples/example_usage.ipynb"
```
