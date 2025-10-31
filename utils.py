"""
Utility functions for SOM Monitor
"""
import json
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd
from pathlib import Path


def format_timestamp(timestamp: str) -> str:
    """Format ISO timestamp to readable string"""
    dt = datetime.fromisoformat(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values"""
    if old_value == 0:
        return 100.0 if new_value > 0 else 0.0
    return ((new_value - old_value) / old_value) * 100


def export_to_csv(data: List[Dict[str, Any]], filename: str) -> None:
    """Export data to CSV file"""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Exported to {filename}")


def export_to_json(data: Any, filename: str, indent: int = 2) -> None:
    """Export data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=indent)
    print(f"Exported to {filename}")


def load_json(filename: str) -> Any:
    """Load data from JSON file"""
    with open(filename, 'r') as f:
        return json.load(f)


def ensure_directory(path: str) -> Path:
    """Ensure directory exists, create if not"""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def validate_api_key(api_key: str, provider: str) -> bool:
    """Validate API key format"""
    if not api_key or api_key.startswith("your-"):
        print(f"❌ Invalid {provider} API key. Please set a valid key.")
        return False
    return True


def color_gradient(value: float, min_val: float = 0.0, max_val: float = 1.0) -> str:
    """
    Generate color based on value (green for high, red for low)
    Returns hex color code
    """
    # Normalize value to 0-1 range
    if max_val == min_val:
        normalized = 0.5
    else:
        normalized = (value - min_val) / (max_val - min_val)
    
    # Simple red to green gradient
    if normalized < 0.5:
        # Red to yellow
        r = 255
        g = int(255 * (normalized * 2))
        b = 0
    else:
        # Yellow to green
        r = int(255 * (1 - (normalized - 0.5) * 2))
        g = 255
        b = 0
    
    return f"#{r:02x}{g:02x}{b:02x}"


def rank_items(items: List[Any], key_func, reverse: bool = True) -> List[tuple]:
    """
    Rank items and return list of (rank, item) tuples
    
    Args:
        items: List of items to rank
        key_func: Function to extract comparison value
        reverse: If True, higher values get better ranks
    
    Returns:
        List of (rank, item) tuples
    """
    sorted_items = sorted(items, key=key_func, reverse=reverse)
    return [(i + 1, item) for i, item in enumerate(sorted_items)]


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Deep merge two dictionaries"""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def batch_items(items: List[Any], batch_size: int) -> List[List[Any]]:
    """Split list into batches"""
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide, returning default if denominator is zero"""
    return numerator / denominator if denominator != 0 else default


def parse_date_range(start_date: str, end_date: str) -> tuple:
    """Parse date range strings to datetime objects"""
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    return start, end


def format_number(value: float, decimals: int = 2) -> str:
    """Format number with thousand separators"""
    return f"{value:,.{decimals}f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format value as percentage"""
    return f"{value * 100:.{decimals}f}%"
