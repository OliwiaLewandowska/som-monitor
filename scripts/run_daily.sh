#!/bin/bash

# Daily SOM Monitor Survey Script
# Add to crontab for automated runs:
# 0 9 * * * /path/to/som-monitor/scripts/run_daily.sh

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/daily_$(date +%Y%m%d).log"

# Create log directory
mkdir -p "$LOG_DIR"

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "======================================"
log "Starting Daily SOM Survey"
log "======================================"

# Change to project directory
cd "$PROJECT_DIR" || exit 1
log "Working directory: $PROJECT_DIR"

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    log "Virtual environment activated"
else
    log "ERROR: Virtual environment not found"
    exit 1
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
    log "Environment variables loaded"
else
    log "ERROR: .env file not found"
    exit 1
fi

# Check API key
if [ -z "$OPENAI_API_KEY" ]; then
    log "ERROR: OPENAI_API_KEY not set"
    exit 1
fi

# Run survey
log "Running survey..."
python main.py \
    --categories general code enterprise reasoning \
    --runs 3 \
    --models gpt-4o \
    >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    log "✓ Survey completed successfully"
else
    log "✗ Survey failed"
    exit 1
fi

# Optional: Send notification (uncomment and configure)
# curl -X POST "YOUR_WEBHOOK_URL" \
#     -H "Content-Type: application/json" \
#     -d '{"text":"Daily SOM survey completed"}' \
#     >> "$LOG_FILE" 2>&1

log "======================================"
log "Daily Survey Complete"
log "======================================"

# Clean up old logs (keep last 30 days)
find "$LOG_DIR" -name "daily_*.log" -mtime +30 -delete
log "Old logs cleaned up"
